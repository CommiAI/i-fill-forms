# I-Fill-Forms: Conversation-Based Form Filler

## Core Idea
A form filling AI app that listens to your conversations and automatically fills PDF forms.

## How It Works

1. **Upload PDFs** - Single file or batch of files
2. **Press Start** - Agent begins listening to conversation
3. **Agent Fills Forms** - As it hears relevant information:
   - Reads the PDF (including images/scanned forms)
   - Identifies which field to fill
   - Gets the x,y coordinates of that field
   - Inserts text at those coordinates
4. **Pipeline Intelligence** - When multiple files uploaded:
   - Recognizes similar fields across documents
   - Fills matching fields in all relevant forms
5. **Live Preview** - Frontend displays forms as they're being filled for real-time review

## Technical Flow
```
[Conversation] → [Agent Listens] → [Extracts Info] → [Reads PDF] → [Finds Field Location] → [Fills at (x,y)]
                                                            ↓
                                                    [Checks Other PDFs]
                                                            ↓
                                                    [Fills Similar Fields]
```

## Key Technical Components
- **PDF Reading**: Model should be able to read the pdf as they go
- **Coordinate Mapping**: Identify exact (x,y) positions for text insertion
- **Context Matching**: Link conversation data to form fields
- **Batch Processing**: Recognize similar fields across multiple documents

## Future Enhancement
- **Undo/Revert Feature**: As conversation context becomes clearer, agent can update previously filled fields

## Problem It Solves
Stop filling the same information across multiple forms. Say it once, fill everywhere.

## Tech stacks plan
AI agents - DSPy
Insert text - fitz
Get text coordinates - fitz -> if get text coordinates does not work, might have to just implement fillable fields approach
backend - fastapi
Frontend - svelte kit 