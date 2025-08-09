from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class SchemaCreate(BaseModel):
    name: str
    fields: List[str]

class SchemaResponse(BaseModel):
    id: str
    name: str
    fields: List[str]
    created_at: datetime

class SessionCreate(BaseModel):
    schema_id: str
    name: str

class SessionResponse(BaseModel):
    id: str
    schema_id: str
    name: str
    created_at: datetime

class ProcessRequest(BaseModel):
    session_id: str
    text: str

class ExtractedData(BaseModel):
    field: str
    value: str
    confidence: float