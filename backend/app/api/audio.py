from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
import logging
from datetime import datetime
from app.services.groq_transcription import GroqTranscriptionService
from app.agents.intelligent_extractor import IntelligentExtractor, ActionType
from app.services.mem0_memory import Mem0MemoryService
from app.database import async_session, Session, Schema

logger = logging.getLogger(__name__)

router = APIRouter()

class AudioChunkRequest(BaseModel):
    session_id: str
    audio_data: str  # Base64 encoded audio

class AudioChunkResponse(BaseModel):
    success: bool
    transcription: str = None
    action: str = None
    extracted_fields: dict = {}
    message: str = None

@router.post("/chunk", response_model=AudioChunkResponse)
async def process_audio_chunk(request: AudioChunkRequest):
    """
    Process audio chunk - same as WebSocket but via REST API.
    """
    session_id = request.session_id
    audio_data = request.audio_data
    
    logger.info(f"[{datetime.now().isoformat()}] Processing audio chunk for session: {session_id}")
    
    # Decode base64 audio data
    try:
        audio_bytes = base64.b64decode(audio_data)
        logger.info(f"[{datetime.now().isoformat()}] Decoded audio size: {len(audio_bytes)} bytes")
    except Exception as e:
        logger.error(f"[{datetime.now().isoformat()}] Failed to decode audio: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid audio data: {str(e)}")
    
    # Get session and schema
    async with async_session() as db:
        session = await db.get(Session, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        schema = await db.get(Schema, session.schema_id)
        if not schema:
            raise HTTPException(status_code=404, detail="Schema not found")
        
        fields = schema.fields
    
    # Transcribe audio using Groq Whisper
    transcription_service = GroqTranscriptionService()
    text = await transcription_service.transcribe_audio_chunk(audio_bytes)
    
    if not text:
        logger.info(f"⚠️ No speech detected in audio")
        return AudioChunkResponse(
            success=False,
            message="No speech detected"
        )
    
    logger.info(f"🎤 TRANSCRIPTION: '{text}'")
    
    # Get conversation memory from Mem0
    mem0_service = Mem0MemoryService()
    context = await mem0_service.get_relevant_context(text, str(session_id))
    
    # Run intelligent agent
    intelligent_extractor = IntelligentExtractor()
    result = intelligent_extractor.forward(text, fields, context)
    
    # Log agent action
    action = result['action_type']
    extracted_fields = {}
    
    if action == ActionType.EXTRACT_FIELDS.value:
        logger.info(f"🤖 AGENT ACTION: Extract Fields - {result.get('extracted_fields', {})}")
        extracted_fields = result.get('extracted_fields', {})
    elif action == ActionType.STORE_CONTEXT.value:
        logger.info(f"🤖 AGENT ACTION: Store Context for future reference")
    else:
        logger.info(f"🤖 AGENT ACTION: Ignore (no relevant data)")
    
    # Handle memory and extraction based on action type
    if result["action_type"] == ActionType.EXTRACT_FIELDS.value:
        # Store interaction AND fields in memory
        await mem0_service.add_conversation_memory(
            text=text,
            session_id=str(session_id),
            action_taken=result["action_type"],
            extracted_fields=result["extracted_fields"]
        )
        
        # Store individual field extractions
        for field, field_value in result["extracted_fields"].items():
            await mem0_service.update_field_memory(
                session_id=str(session_id),
                field_name=field,
                field_value=field_value
            )
            logger.info(f"✅ FIELD UPDATE: {field} = '{field_value}'")
    
    elif result["action_type"] == ActionType.STORE_CONTEXT.value:
        # Store context for future reference
        await mem0_service.add_conversation_memory(
            text=text,
            session_id=str(session_id),
            action_taken=result["action_type"]
        )
    
    return AudioChunkResponse(
        success=True,
        transcription=text,
        action=action,
        extracted_fields=extracted_fields,
        message="Audio processed successfully"
    )