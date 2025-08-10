"""
DSPy optimization script for i-fill-forms signatures.
This script optimizes the AgentDecision and FieldExtractor signatures using training data.
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
import dspy
from dspy.teleprompt import BootstrapFewShot, BootstrapFewShotWithRandomSearch, MIPROv2

# Import the signatures from the main module
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from app.agents.intelligent_extractor import AgentDecision, FieldExtractor
from app.config.settings import settings


class DSPyOptimizer:
    """Optimize DSPy signatures for improved performance."""
    
    def __init__(self):
        """Initialize the optimizer with Groq LLM configuration."""
        # Configure DSPy with Groq LLM
        self.groq_lm = dspy.LM(
            "meta/llama-3.3-70b-versatile",
            api_key=settings.groq_api_key,
            api_base="https://api.groq.com/openai/v1"
        )
        dspy.configure(lm=self.groq_lm)
        
        # Paths for models and data
        self.models_dir = Path("backend/app/optimization/models")
        self.data_dir = Path("backend/app/optimization/training_data")
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def load_dataset(self, dataset_path: str) -> List[dspy.Example]:
        """Load JSON dataset and convert to DSPy format."""
        with open(dataset_path, "r") as f:
            data = json.load(f)
        
        examples = []
        for item in data:
            # Detect which type of example based on fields
            if "action_type" in item:
                # AgentDecision example
                example = dspy.Example(
                    conversation_history=item["conversation_history"],
                    current_text=item["current_text"],
                    schema_fields=item["schema_fields"],
                    action_type=item["action_type"],
                    reasoning=item["reasoning"]
                ).with_inputs('conversation_history', 'current_text', 'schema_fields')
            else:
                # FieldExtractor example
                example = dspy.Example(
                    text=item["text"],
                    field_name=item["field_name"],
                    context=item["context"],
                    value=item["value"]
                ).with_inputs('text', 'field_name', 'context')
            
            examples.append(example)
        
        return examples
    
    def decision_metric(self, gold: dspy.Example, pred: dspy.Prediction, trace=None) -> float:
        """
        Metric for evaluating AgentDecision predictions.
        Returns 1.0 for correct action_type, 0.0 otherwise.
        """
        try:
            # Check if the predicted action matches the gold standard
            return 1.0 if gold.action_type.lower() == pred.action_type.lower() else 0.0
        except:
            return 0.0
    
    def extraction_metric(self, gold: dspy.Example, pred: dspy.Prediction, trace=None) -> float:
        """
        Metric for evaluating FieldExtractor predictions.
        Returns 1.0 for exact match, 0.5 for partial match, 0.0 for incorrect.
        """
        try:
            gold_value = gold.value.lower().strip()
            pred_value = pred.value.lower().strip()
            
            # Both are "none" - correct negative
            if gold_value == "none" and pred_value == "none":
                return 1.0
            
            # Exact match
            if gold_value == pred_value:
                return 1.0
            
            # Partial match - predicted contains gold or vice versa
            if gold_value in pred_value or pred_value in gold_value:
                return 0.5
            
            return 0.0
        except:
            return 0.0
    
    def optimize_agent_decision(self, optimizer_type: str = "bootstrap") -> dspy.Module:
        """
        Optimize the AgentDecision signature.
        
        Args:
            optimizer_type: Type of optimizer to use ("bootstrap", "bootstrap_random", "mipro")
        
        Returns:
            Optimized DSPy module
        """
        print("📊 Optimizing AgentDecision signature...")
        
        # Load training and validation data
        train_data = self.load_dataset(self.data_dir / "agent_decision" / "train.json")
        val_data = self.load_dataset(self.data_dir / "agent_decision" / "val.json")
        
        print(f"   Loaded {len(train_data)} training examples, {len(val_data)} validation examples")
        
        # Define the program to optimize
        class DecisionProgram(dspy.Module):
            def __init__(self):
                super().__init__()
                self.prog = dspy.ChainOfThought(AgentDecision)
            
            def forward(self, conversation_history, current_text, schema_fields):
                return self.prog(
                    conversation_history=conversation_history,
                    current_text=current_text,
                    schema_fields=schema_fields
                )
        
        program = DecisionProgram()
        
        # Choose optimizer
        if optimizer_type == "bootstrap":
            print("   Using BootstrapFewShot optimizer...")
            optimizer = BootstrapFewShot(
                metric=self.decision_metric,
                max_bootstrapped_demos=4,  # Number of examples to include in prompt
                max_labeled_demos=16,       # Pool of examples to choose from
                max_rounds=1,
                max_errors=5
            )
        elif optimizer_type == "bootstrap_random":
            print("   Using BootstrapFewShotWithRandomSearch optimizer...")
            optimizer = BootstrapFewShotWithRandomSearch(
                metric=self.decision_metric,
                max_bootstrapped_demos=4,
                max_labeled_demos=16,
                num_candidate_programs=10,  # Try 10 different prompt variations
                num_threads=4
            )
        elif optimizer_type == "mipro":
            print("   Using MIPROv2 optimizer (this may take longer)...")
            optimizer = MIPROv2(
                metric=self.decision_metric,
                auto="light",  # Use light mode for faster optimization
                num_trials=10,
                init_temperature=1.0
            )
        else:
            raise ValueError(f"Unknown optimizer type: {optimizer_type}")
        
        # Run optimization
        optimized_program = optimizer.compile(
            program,
            trainset=train_data,
            valset=val_data
        )
        
        # Evaluate on validation set
        print("\n   Evaluating optimized program...")
        correct = 0
        for example in val_data[:20]:  # Test on subset for speed
            pred = optimized_program(
                conversation_history=example.conversation_history,
                current_text=example.current_text,
                schema_fields=example.schema_fields
            )
            score = self.decision_metric(example, pred)
            correct += score
        
        accuracy = correct / min(20, len(val_data))
        print(f"   ✅ Validation accuracy: {accuracy:.2%}")
        
        # Save the optimized program
        model_path = self.models_dir / f"optimized_decision_{optimizer_type}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(optimized_program, f)
        print(f"   💾 Saved optimized model to {model_path}")
        
        return optimized_program
    
    def optimize_field_extractor(self, optimizer_type: str = "bootstrap") -> dspy.Module:
        """
        Optimize the FieldExtractor signature.
        
        Args:
            optimizer_type: Type of optimizer to use ("bootstrap", "bootstrap_random", "mipro")
        
        Returns:
            Optimized DSPy module
        """
        print("📊 Optimizing FieldExtractor signature...")
        
        # Load training and validation data
        train_data = self.load_dataset(self.data_dir / "field_extractor" / "train.json")
        val_data = self.load_dataset(self.data_dir / "field_extractor" / "val.json")
        
        print(f"   Loaded {len(train_data)} training examples, {len(val_data)} validation examples")
        
        # Define the program to optimize
        class ExtractorProgram(dspy.Module):
            def __init__(self):
                super().__init__()
                self.prog = dspy.ChainOfThought(FieldExtractor)
            
            def forward(self, text, field_name, context):
                return self.prog(
                    text=text,
                    field_name=field_name,
                    context=context
                )
        
        program = ExtractorProgram()
        
        # Choose optimizer
        if optimizer_type == "bootstrap":
            print("   Using BootstrapFewShot optimizer...")
            optimizer = BootstrapFewShot(
                metric=self.extraction_metric,
                max_bootstrapped_demos=4,
                max_labeled_demos=16,
                max_rounds=1,
                max_errors=5
            )
        elif optimizer_type == "bootstrap_random":
            print("   Using BootstrapFewShotWithRandomSearch optimizer...")
            optimizer = BootstrapFewShotWithRandomSearch(
                metric=self.extraction_metric,
                max_bootstrapped_demos=4,
                max_labeled_demos=16,
                num_candidate_programs=10,
                num_threads=4
            )
        elif optimizer_type == "mipro":
            print("   Using MIPROv2 optimizer (this may take longer)...")
            optimizer = MIPROv2(
                metric=self.extraction_metric,
                auto="light",
                num_trials=10,
                init_temperature=1.0
            )
        else:
            raise ValueError(f"Unknown optimizer type: {optimizer_type}")
        
        # Run optimization
        optimized_program = optimizer.compile(
            program,
            trainset=train_data,
            valset=val_data
        )
        
        # Evaluate on validation set
        print("\n   Evaluating optimized program...")
        scores = []
        for example in val_data[:20]:  # Test on subset for speed
            pred = optimized_program(
                text=example.text,
                field_name=example.field_name,
                context=example.context
            )
            score = self.extraction_metric(example, pred)
            scores.append(score)
        
        avg_score = sum(scores) / len(scores)
        print(f"   ✅ Validation score: {avg_score:.2f}/1.0")
        
        # Save the optimized program
        model_path = self.models_dir / f"optimized_extractor_{optimizer_type}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(optimized_program, f)
        print(f"   💾 Saved optimized model to {model_path}")
        
        return optimized_program
    
    def evaluate_baseline(self):
        """Evaluate the baseline (non-optimized) performance."""
        print("📊 Evaluating baseline performance...")
        
        # Evaluate AgentDecision baseline
        print("\n🔍 AgentDecision baseline:")
        decision_val = self.load_dataset(self.data_dir / "agent_decision" / "val.json")
        decision_program = dspy.ChainOfThought(AgentDecision)
        
        correct = 0
        for example in decision_val[:20]:
            pred = decision_program(
                conversation_history=example.conversation_history,
                current_text=example.current_text,
                schema_fields=example.schema_fields
            )
            score = self.decision_metric(example, pred)
            correct += score
        
        accuracy = correct / min(20, len(decision_val))
        print(f"   Baseline accuracy: {accuracy:.2%}")
        
        # Evaluate FieldExtractor baseline
        print("\n🔍 FieldExtractor baseline:")
        extractor_val = self.load_dataset(self.data_dir / "field_extractor" / "val.json")
        extractor_program = dspy.ChainOfThought(FieldExtractor)
        
        scores = []
        for example in extractor_val[:20]:
            pred = extractor_program(
                text=example.text,
                field_name=example.field_name,
                context=example.context
            )
            score = self.extraction_metric(example, pred)
            scores.append(score)
        
        avg_score = sum(scores) / len(scores)
        print(f"   Baseline score: {avg_score:.2f}/1.0")
    
    def run_full_optimization(self, optimizer_type: str = "bootstrap"):
        """Run the full optimization pipeline."""
        print("🚀 Starting DSPy optimization pipeline...\n")
        
        # Check if training data exists
        if not (self.data_dir / "agent_decision" / "train.json").exists():
            print("⚠️  Training data not found. Please run create_training_data.py first.")
            return
        
        # Evaluate baseline
        self.evaluate_baseline()
        
        print("\n" + "="*50 + "\n")
        
        # Optimize AgentDecision
        optimized_decision = self.optimize_agent_decision(optimizer_type)
        
        print("\n" + "="*50 + "\n")
        
        # Optimize FieldExtractor
        optimized_extractor = self.optimize_field_extractor(optimizer_type)
        
        print("\n" + "="*50)
        print("✨ Optimization complete!")
        print(f"   Models saved to {self.models_dir}")
        print("\n📈 Performance improvements:")
        print("   AgentDecision: Check validation accuracy above")
        print("   FieldExtractor: Check validation score above")
        print("\n💡 To use optimized models, update IntelligentExtractor to load from:")
        print(f"   - {self.models_dir}/optimized_decision_{optimizer_type}.pkl")
        print(f"   - {self.models_dir}/optimized_extractor_{optimizer_type}.pkl")


def main():
    """Main entry point for optimization script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimize DSPy signatures for i-fill-forms")
    parser.add_argument(
        "--optimizer",
        type=str,
        default="bootstrap",
        choices=["bootstrap", "bootstrap_random", "mipro"],
        help="Type of optimizer to use"
    )
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Only evaluate baseline performance without optimization"
    )
    
    args = parser.parse_args()
    
    optimizer = DSPyOptimizer()
    
    if args.baseline_only:
        optimizer.evaluate_baseline()
    else:
        optimizer.run_full_optimization(args.optimizer)


if __name__ == "__main__":
    main()