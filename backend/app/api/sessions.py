from fastapi import APIRouter, HTTPException
from app.database import async_session, Session, Schema, SessionData
from app.models.schema import SessionCreate, SessionResponse
from sqlalchemy import select
from typing import List

router = APIRouter()

@router.post("/create", response_model=SessionResponse)
async def create_session(session_data: SessionCreate):
    async with async_session() as db:
        # Verify schema exists
        schema = await db.get(Schema, session_data.schema_id)
        if not schema:
            raise HTTPException(status_code=404, detail="Schema not found")
        
        session = Session(
            schema_id=session_data.schema_id,
            name=session_data.name
        )
        db.add(session)
        await db.commit()
        
        return SessionResponse(
            id=session.id,
            schema_id=session.schema_id,
            name=session.name,
            created_at=session.created_at
        )

@router.get("/list", response_model=List[SessionResponse])
async def list_sessions():
    async with async_session() as db:
        result = await db.execute(select(Session))
        sessions = result.scalars().all()
        return [SessionResponse(
            id=s.id,
            schema_id=s.schema_id,
            name=s.name,
            created_at=s.created_at
        ) for s in sessions]

@router.get("/{session_id}")
async def get_session(session_id: str):
    async with async_session() as db:
        session = await db.get(Session, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get session data
        result = await db.execute(
            select(SessionData).where(SessionData.session_id == session_id)
        )
        data = result.scalars().all()
        
        return {
            "id": session.id,
            "schema_id": session.schema_id,
            "name": session.name,
            "data": [d.data for d in data],
            "created_at": session.created_at
        }