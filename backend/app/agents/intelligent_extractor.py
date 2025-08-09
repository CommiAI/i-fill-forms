import dspy
import os
from typing import Dict, List, Optional, Tuple
from enum import Enum
from app.config.settings import settings

class ActionType(Enum):
    EXTRACT_FIELDS = "extract_fields"  # Extract fields AND store in memory
    STORE_CONTEXT = "store_context"    # Store context only, no extraction
    IGNORE = "ignore"                  # Neither store nor extract

class AgentDecision(dspy.Signature):
    """Analyze conversation text and decide what action to take."""
    
    conversation_history: str = dspy.InputField(desc="Previous conversation context")
    current_text: str = dspy.InputField(desc="Current audio transcription")
    schema_fields: str = dspy.InputField(desc="Available form fields to fill")
    
    action_type: str = dspy.OutputField(desc="Action to take: extract_fields, store_context, or ignore")
    reasoning: str = dspy.OutputField(desc="Explanation for the decision")

class FieldExtractor(dspy.Signature):
    """Extract specific field values from conversation text."""
    
    text: str = dspy.InputField(desc="Conversation text to analyze")
    field_name: str = dspy.InputField(desc="Specific field to extract (e.g., 'name', 'email')")
    context: str = dspy.InputField(desc="Additional context from conversation")
    
    value: str = dspy.OutputField(desc="Extracted field value or 'none' if not found")

class IntelligentExtractor(dspy.Module):
    def __init__(self):
        # Configure DSPy to use Groq LLM for agent reasoning
        groq_lm = dspy.LM(
            "qwen/qwen3-32b", 
            api_key=settings.groq_api_key,
            api_base="https://api.groq.com/openai/v1"
        )
        # Set the LM globally for DSPy
        dspy.configure(lm=groq_lm)
        
        self.decide_action = dspy.ChainOfThought(AgentDecision)
        self.extract_field = dspy.ChainOfThought(FieldExtractor)
    
    def forward(self, text: str, fields: List[str], mem0_context: str = "") -> Dict:
        # Make decision about what to do
        schema_fields_str = ", ".join(fields)
        decision = self.decide_action(
            conversation_history=mem0_context,
            current_text=text,
            schema_fields=schema_fields_str
        )
        
        result = {
            "action_type": decision.action_type,
            "reasoning": decision.reasoning,
            "extracted_fields": {}
        }
        
        if decision.action_type == ActionType.EXTRACT_FIELDS.value:
            # Extract fields for schema AND store in memory
            for field in fields:
                extraction = self.extract_field(
                    text=text,
                    field_name=field,
                    context=mem0_context
                )
                if extraction.value.lower() != "none":
                    result["extracted_fields"][field] = extraction.value
        
        return result