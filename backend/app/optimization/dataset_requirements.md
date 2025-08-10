# DSPy Training Dataset Requirements for i-fill-forms

## Overview
This document defines the exact dataset format and fields required to train and optimize the DSPy signatures in the i-fill-forms application.

## Required Dataset Structures

### 1. AgentDecision Training Data

Each training example must contain:

```python
{
    "conversation_history": str,  # Previous conversation context from Mem0
    "current_text": str,          # Current audio transcription chunk
    "schema_fields": str,         # Comma-separated list of form fields (e.g., "name, email, phone, age, condition")
    "action_type": str,           # Ground truth: "extract_fields" | "store_context" | "ignore"
    "reasoning": str              # Explanation for why this action was chosen
}
```

#### Example Training Instances:

```json
[
    {
        "conversation_history": "",
        "current_text": "Hello, my name is Sarah Johnson",
        "schema_fields": "name, email, phone, date_of_birth, medical_condition",
        "action_type": "extract_fields",
        "reasoning": "User provided their name which matches the 'name' field in the schema"
    },
    {
        "conversation_history": "User mentioned they have diabetes",
        "current_text": "I've been taking metformin for about 3 years now",
        "schema_fields": "name, email, phone, medication, condition",
        "action_type": "store_context",
        "reasoning": "Medication information is relevant context but not directly extractable to current fields"
    },
    {
        "conversation_history": "User's name is John Smith",
        "current_text": "Um, let me think about that",
        "schema_fields": "name, email, phone, age",
        "action_type": "ignore",
        "reasoning": "Filler speech with no extractable information"
    }
]
```

### 2. FieldExtractor Training Data

Each training example must contain:

```python
{
    "text": str,         # Conversation text to analyze
    "field_name": str,   # Specific field to extract (e.g., 'name', 'email')
    "context": str,      # Additional context from conversation history
    "value": str         # Ground truth: extracted value or "none" if not found
}
```

#### Example Training Instances:

```json
[
    {
        "text": "My email is sarah.johnson@example.com",
        "field_name": "email",
        "context": "User is providing contact information",
        "value": "sarah.johnson@example.com"
    },
    {
        "text": "I'm 45 years old",
        "field_name": "age",
        "context": "",
        "value": "45"
    },
    {
        "text": "I work as a software engineer",
        "field_name": "email",
        "context": "User discussing their profession",
        "value": "none"
    },
    {
        "text": "You can call me at 555-123-4567",
        "field_name": "phone",
        "context": "User providing contact details",
        "value": "555-123-4567"
    }
]
```

## Dataset Categories to Include

### 1. Direct Extractions (40% of dataset)
- Clear, unambiguous statements
- "My name is X", "My email is Y", "I am Z years old"
- Various phrasings for common fields

### 2. Contextual Extractions (30% of dataset)
- Information requiring context
- "It's Sarah" (after being asked for name)
- "45" (in response to age question)
- Pronouns and references

### 3. Negative Examples (20% of dataset)
- Text with no extractable information
- Filler speech ("um", "uh", "let me think")
- Off-topic conversations
- Information that doesn't match any field

### 4. Edge Cases (10% of dataset)
- Ambiguous information
- Multiple values in one utterance
- Corrections ("Actually, it's not John, it's Jonathan")
- Partial information

## Field Types to Cover

Based on the current implementation, prepare examples for these common form fields:

1. **Personal Information**
   - name (full name, first name, last name)
   - email
   - phone (various formats)
   - date_of_birth / age
   - address (street, city, state, zip)
   - ssn (last 4 digits only for privacy)

2. **Medical Information**
   - condition / diagnosis
   - medication
   - allergies
   - symptoms
   - doctor_name
   - insurance_provider
   - policy_number

3. **Appointment/Administrative**
   - appointment_date
   - appointment_time
   - reason_for_visit
   - referring_physician
   - emergency_contact

## Data Collection Methods

### 1. Manual Creation (Quick Start - 50 examples)
Create a diverse set of examples manually covering:
- Common extraction patterns
- Various phrasings for each field
- Clear positive and negative examples

### 2. Synthetic Generation (Scale to 200+ examples)
```python
# Example synthetic data generator
import random
from typing import List, Dict

class TrainingDataGenerator:
    def __init__(self):
        self.name_templates = [
            "My name is {name}",
            "I'm {name}",
            "This is {name}",
            "You can call me {name}",
            "{name} here"
        ]
        self.email_templates = [
            "My email is {email}",
            "You can reach me at {email}",
            "Email me at {email}",
            "{email} is my email address"
        ]
        # Add more templates...
    
    def generate_examples(self, count: int) -> List[Dict]:
        examples = []
        # Generate varied examples using templates
        return examples
```

### 3. Real Usage Data (Continuous Improvement)
- Capture successful extractions from production usage
- Use Mem0 memory service to log interactions
- Require user confirmation for training data inclusion

## Evaluation Metrics

### For AgentDecision:
- **Accuracy**: Correct action_type classification (extract/store/ignore)
- **Precision**: When predicting "extract_fields", is there actually something to extract?
- **Recall**: Are we catching all extractable information?

### For FieldExtractor:
- **Exact Match**: Extracted value exactly matches ground truth
- **Partial Match**: Extracted value contains the correct information
- **Format Consistency**: Phone numbers, dates formatted correctly
- **False Positive Rate**: Extracting wrong information vs returning "none"

## Dataset Size Requirements

### Minimum Viable Dataset:
- 50 examples per signature for initial testing
- 25 positive examples (successful extractions)
- 15 negative examples (ignore/none cases)
- 10 edge cases

### Production-Ready Dataset:
- 200-500 examples per signature
- Balanced across all field types
- Representative of real conversation patterns
- Include domain-specific medical terminology

## Format for DSPy

Convert datasets to DSPy format:

```python
import dspy

# For AgentDecision
decision_examples = []
for item in decision_dataset:
    example = dspy.Example(
        conversation_history=item["conversation_history"],
        current_text=item["current_text"],
        schema_fields=item["schema_fields"],
        action_type=item["action_type"],
        reasoning=item["reasoning"]
    ).with_inputs('conversation_history', 'current_text', 'schema_fields')
    decision_examples.append(example)

# For FieldExtractor
extraction_examples = []
for item in extraction_dataset:
    example = dspy.Example(
        text=item["text"],
        field_name=item["field_name"],
        context=item["context"],
        value=item["value"]
    ).with_inputs('text', 'field_name', 'context')
    extraction_examples.append(example)
```

## Next Steps

1. Create `training_data/` directory structure:
   ```
   backend/app/optimization/training_data/
   ├── agent_decision/
   │   ├── train.json
   │   └── val.json
   └── field_extractor/
       ├── train.json
       └── val.json
   ```

2. Start with manual creation of 50 high-quality examples

3. Build synthetic data generator for scaling

4. Implement data validation to ensure quality

5. Create scripts to convert JSON to DSPy format

## Privacy and Compliance

- Never use real patient data without proper anonymization
- Synthetic data should not contain real PII
- Follow HIPAA guidelines for any healthcare data
- Implement data retention policies for training data