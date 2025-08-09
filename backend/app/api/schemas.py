from fastapi import APIRouter, UploadFile, File, HTTPException
from app.database import async_session, Schema
from app.models.schema import SchemaCreate, SchemaResponse
from app.services.csv_handler import extract_fields_from_csv, validate_csv_structure
from sqlalchemy import select
from typing import List

router = APIRouter()

@router.post("/upload", response_model=SchemaResponse)
async def upload_schema(file: UploadFile = File(...)):
    content = await file.read()
    
    if not validate_csv_structure(content):
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    
    fields = extract_fields_from_csv(content)
    
    async with async_session() as session:
        schema = Schema(
            name=file.filename.replace('.csv', ''),
            fields=fields
        )
        session.add(schema)
        await session.commit()
        
        return SchemaResponse(
            id=schema.id,
            name=schema.name,
            fields=schema.fields,
            created_at=schema.created_at
        )

@router.get("/list", response_model=List[SchemaResponse])
async def list_schemas():
    async with async_session() as session:
        result = await session.execute(select(Schema))
        schemas = result.scalars().all()
        return [SchemaResponse(
            id=s.id,
            name=s.name,
            fields=s.fields,
            created_at=s.created_at
        ) for s in schemas]

@router.get("/{schema_id}", response_model=SchemaResponse)
async def get_schema(schema_id: str):
    async with async_session() as session:
        schema = await session.get(Schema, schema_id)
        if not schema:
            raise HTTPException(status_code=404, detail="Schema not found")
        return SchemaResponse(
            id=schema.id,
            name=schema.name,
            fields=schema.fields,
            created_at=schema.created_at
        )