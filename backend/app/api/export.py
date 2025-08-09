from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.database import async_session, Session, Schema, SessionData
from sqlalchemy import select
import pandas as pd
from io import StringIO

router = APIRouter()

@router.get("/{session_id}/csv")
async def export_csv(session_id: str):
    async with async_session() as db:
        # Get session and schema
        session = await db.get(Session, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        schema = await db.get(Schema, session.schema_id)
        
        # Get all data for session
        result = await db.execute(
            select(SessionData).where(SessionData.session_id == session_id)
        )
        data_rows = result.scalars().all()
        
        # Create DataFrame
        if data_rows:
            df = pd.DataFrame([row.data for row in data_rows])
            # Ensure all schema fields are present
            for field in schema.fields:
                if field not in df.columns:
                    df[field] = ""
            df = df[schema.fields]  # Reorder columns
        else:
            # Empty DataFrame with schema columns
            df = pd.DataFrame(columns=schema.fields)
        
        # Convert to CSV
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={session.name}.csv"
            }
        )