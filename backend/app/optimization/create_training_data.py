"""
Script to create training datasets for DSPy optimization of i-fill-forms.
This generates synthetic training data for both AgentDecision and FieldExtractor signatures.
"""

import json
import random
from typing import List, Dict, Tuple
from pathlib import Path
import dspy


class TrainingDataGenerator:
    """Generate synthetic training data for DSPy optimization."""
    
    def __init__(self):
        # Sample data for generation
        self.first_names = ["John", "Sarah", "Michael", "Emily", "David", "Jessica", "Robert", "Lisa", "James", "Maria"]
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        self.domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "email.com"]
        self.conditions = ["diabetes", "hypertension", "asthma", "arthritis", "migraine", "anxiety", "back pain"]
        self.medications = ["metformin", "lisinopril", "albuterol", "ibuprofen", "aspirin", "insulin", "omeprazole"]
        
        # Common form fields
        self.common_fields = [
            "name", "email", "phone", "age", "date_of_birth",
            "address", "condition", "medication", "doctor_name",
            "insurance_provider", "policy_number", "emergency_contact"
        ]
        
        # Templates for different types of utterances
        self.name_templates = [
            "My name is {first} {last}",
            "I'm {first} {last}",
            "This is {first} {last} speaking",
            "You can call me {first}",
            "{first} {last}, that's my name",
            "The name is {last}, {first} {last}"
        ]
        
        self.email_templates = [
            "My email is {email}",
            "You can reach me at {email}",
            "Email me at {email}",
            "{email} is my email address",
            "My email address is {email}"
        ]
        
        self.phone_templates = [
            "My phone number is {phone}",
            "You can call me at {phone}",
            "My number is {phone}",
            "Call me on {phone}",
            "I can be reached at {phone}"
        ]
        
        self.age_templates = [
            "I'm {age} years old",
            "I am {age}",
            "Age {age}",
            "I'm {age} years of age",
            "I'll be {age} next month"
        ]
        
        self.condition_templates = [
            "I have {condition}",
            "I was diagnosed with {condition}",
            "I suffer from {condition}",
            "My condition is {condition}",
            "I'm being treated for {condition}"
        ]
        
        self.filler_phrases = [
            "Um, let me think about that",
            "Uh, I'm not sure",
            "Well, you know",
            "So, basically",
            "Let me see",
            "Actually, wait",
            "Oh, I forgot to mention",
            "By the way",
            "One more thing"
        ]

    def generate_phone_number(self) -> str:
        """Generate a random phone number in various formats."""
        formats = [
            "{}-{}-{}",
            "({}) {}-{}",
            "{}.{}.{}",
            "{}{}{}"
        ]
        area = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        
        format_choice = random.choice(formats)
        if "(" in format_choice:
            return format_choice.format(area, prefix, line)
        else:
            return format_choice.format(area, prefix, line)

    def generate_email(self, first_name: str, last_name: str) -> str:
        """Generate an email address based on name."""
        patterns = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{random.randint(1, 99)}"
        ]
        return f"{random.choice(patterns)}@{random.choice(self.domains)}"

    def generate_agent_decision_examples(self, count: int = 100) -> List[Dict]:
        """Generate training examples for AgentDecision signature."""
        examples = []
        
        # Generate positive examples (extract_fields)
        for _ in range(count // 2):
            first = random.choice(self.first_names)
            last = random.choice(self.last_names)
            
            # Vary the complexity of schema fields
            num_fields = random.randint(3, 7)
            fields = random.sample(self.common_fields, num_fields)
            schema_fields = ", ".join(fields)
            
            # Generate different types of extractable content
            extract_types = ["name", "email", "phone", "age", "condition"]
            extract_type = random.choice(extract_types)
            
            if extract_type == "name":
                template = random.choice(self.name_templates)
                current_text = template.format(first=first, last=last)
                reasoning = "User provided their name which matches the 'name' field in the schema"
            elif extract_type == "email":
                email = self.generate_email(first, last)
                template = random.choice(self.email_templates)
                current_text = template.format(email=email)
                reasoning = "User provided their email address which matches the 'email' field"
            elif extract_type == "phone":
                phone = self.generate_phone_number()
                template = random.choice(self.phone_templates)
                current_text = template.format(phone=phone)
                reasoning = "User provided their phone number which matches the 'phone' field"
            elif extract_type == "age":
                age = random.randint(18, 90)
                template = random.choice(self.age_templates)
                current_text = template.format(age=age)
                reasoning = "User provided their age which matches the 'age' field"
            else:  # condition
                condition = random.choice(self.conditions)
                template = random.choice(self.condition_templates)
                current_text = template.format(condition=condition)
                reasoning = "User mentioned a medical condition which matches the 'condition' field"
            
            # Add some conversation history randomly
            conversation_history = ""
            if random.random() > 0.5:
                conversation_history = f"User previously mentioned they live in California"
            
            examples.append({
                "conversation_history": conversation_history,
                "current_text": current_text,
                "schema_fields": schema_fields,
                "action_type": "extract_fields",
                "reasoning": reasoning
            })
        
        # Generate store_context examples
        for _ in range(count // 4):
            medication = random.choice(self.medications)
            context_phrases = [
                f"I've been taking {medication} for years",
                f"My doctor prescribed {medication}",
                f"I'm allergic to {medication}",
                f"I prefer morning appointments",
                f"I have insurance through my employer",
                f"I've been seeing Dr. Smith for this"
            ]
            
            fields = random.sample(self.common_fields, random.randint(3, 5))
            schema_fields = ", ".join(fields)
            
            examples.append({
                "conversation_history": random.choice(["", "Previous context about user's medical history"]),
                "current_text": random.choice(context_phrases),
                "schema_fields": schema_fields,
                "action_type": "store_context",
                "reasoning": "Information is relevant for context but doesn't directly match current fields"
            })
        
        # Generate ignore examples
        for _ in range(count // 4):
            fields = random.sample(self.common_fields, random.randint(3, 5))
            schema_fields = ", ".join(fields)
            
            examples.append({
                "conversation_history": "",
                "current_text": random.choice(self.filler_phrases),
                "schema_fields": schema_fields,
                "action_type": "ignore",
                "reasoning": "Filler speech with no extractable information"
            })
        
        return examples

    def generate_field_extractor_examples(self, count: int = 100) -> List[Dict]:
        """Generate training examples for FieldExtractor signature."""
        examples = []
        
        for _ in range(count):
            first = random.choice(self.first_names)
            last = random.choice(self.last_names)
            
            # Randomly choose what to extract
            field_type = random.choice(["name", "email", "phone", "age", "condition", "none"])
            
            if field_type == "name":
                template = random.choice(self.name_templates)
                text = template.format(first=first, last=last)
                
                # Generate examples for extracting name
                examples.append({
                    "text": text,
                    "field_name": "name",
                    "context": "",
                    "value": f"{first} {last}"
                })
                
                # Also generate negative example
                examples.append({
                    "text": text,
                    "field_name": "email",
                    "context": "",
                    "value": "none"
                })
                
            elif field_type == "email":
                email = self.generate_email(first, last)
                template = random.choice(self.email_templates)
                text = template.format(email=email)
                
                examples.append({
                    "text": text,
                    "field_name": "email",
                    "context": "User providing contact information",
                    "value": email
                })
                
            elif field_type == "phone":
                phone = self.generate_phone_number()
                template = random.choice(self.phone_templates)
                text = template.format(phone=phone)
                
                examples.append({
                    "text": text,
                    "field_name": "phone",
                    "context": "",
                    "value": phone
                })
                
            elif field_type == "age":
                age = random.randint(18, 90)
                template = random.choice(self.age_templates)
                text = template.format(age=age)
                
                examples.append({
                    "text": text,
                    "field_name": "age",
                    "context": "",
                    "value": str(age)
                })
                
            elif field_type == "condition":
                condition = random.choice(self.conditions)
                template = random.choice(self.condition_templates)
                text = template.format(condition=condition)
                
                examples.append({
                    "text": text,
                    "field_name": "condition",
                    "context": "Medical history discussion",
                    "value": condition
                })
                
            else:  # none
                text = random.choice(self.filler_phrases)
                field = random.choice(self.common_fields)
                
                examples.append({
                    "text": text,
                    "field_name": field,
                    "context": "",
                    "value": "none"
                })
        
        return examples

    def save_datasets(self, decision_examples: List[Dict], extractor_examples: List[Dict], 
                      output_dir: str = "backend/app/optimization/training_data"):
        """Save datasets to JSON files with train/validation split."""
        output_path = Path(output_dir)
        
        # Create directory structure
        decision_dir = output_path / "agent_decision"
        extractor_dir = output_path / "field_extractor"
        decision_dir.mkdir(parents=True, exist_ok=True)
        extractor_dir.mkdir(parents=True, exist_ok=True)
        
        # Split datasets (80% train, 20% validation)
        def split_data(data: List[Dict], train_ratio: float = 0.8) -> Tuple[List[Dict], List[Dict]]:
            random.shuffle(data)
            split_idx = int(len(data) * train_ratio)
            return data[:split_idx], data[split_idx:]
        
        # Save AgentDecision datasets
        decision_train, decision_val = split_data(decision_examples)
        with open(decision_dir / "train.json", "w") as f:
            json.dump(decision_train, f, indent=2)
        with open(decision_dir / "val.json", "w") as f:
            json.dump(decision_val, f, indent=2)
        
        # Save FieldExtractor datasets
        extractor_train, extractor_val = split_data(extractor_examples)
        with open(extractor_dir / "train.json", "w") as f:
            json.dump(extractor_train, f, indent=2)
        with open(extractor_dir / "val.json", "w") as f:
            json.dump(extractor_val, f, indent=2)
        
        print(f"✅ Datasets saved to {output_path}")
        print(f"   AgentDecision: {len(decision_train)} train, {len(decision_val)} val")
        print(f"   FieldExtractor: {len(extractor_train)} train, {len(extractor_val)} val")

    def load_and_convert_to_dspy(self, dataset_path: str) -> List[dspy.Example]:
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


def main():
    """Generate training datasets for DSPy optimization."""
    generator = TrainingDataGenerator()
    
    print("🚀 Generating training data for DSPy optimization...")
    
    # Generate examples
    decision_examples = generator.generate_agent_decision_examples(count=200)
    extractor_examples = generator.generate_field_extractor_examples(count=200)
    
    # Save to files
    generator.save_datasets(decision_examples, extractor_examples)
    
    # Demonstrate loading and converting to DSPy format
    print("\n📚 Loading and converting to DSPy format...")
    decision_train_dspy = generator.load_and_convert_to_dspy(
        "backend/app/optimization/training_data/agent_decision/train.json"
    )
    print(f"   Loaded {len(decision_train_dspy)} AgentDecision training examples")
    
    # Show sample
    print("\n📝 Sample AgentDecision DSPy example:")
    if decision_train_dspy:
        sample = decision_train_dspy[0]
        print(f"   Inputs: {sample.inputs()}")
        print(f"   Labels: action_type={sample.action_type}, reasoning={sample.reasoning}")


if __name__ == "__main__":
    main()