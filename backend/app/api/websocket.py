from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.database import async_session, Session, Schema, SessionData
from app.agents.extractor import extractor
from app.agents.intelligent_extractor import IntelligentExtractor, ActionType
from app.services.groq_transcription import GroqTranscriptionService
from app.services.mem0_memory import Mem0MemoryService
from typing import Dict, List
import json
import base64
from datetime import datetime
from sqlalchemy import select
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def send_field_update(self, session_id: str, field: str, value: str):
        """Send real-time field update to React frontend"""
        if session_id in self.active_connections:
            message = json.dumps({
                "type": "field_update",
                "field": field,
                "value": value,
                "timestamp": datetime.now().isoformat()
            })
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    # Handle disconnected clients
                    logger.warning(f"[{datetime.now().isoformat()}] Failed to send to connection: {str(e)}")

    async def send_status(self, session_id: str, status: str, message: str = ""):
        """Send processing status updates"""
        if session_id in self.active_connections:
            msg = json.dumps({
                "type": "status",
                "status": status,  # "processing", "ready", "error"
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(msg)
                except Exception as e:
                    logger.warning(f"[{datetime.now().isoformat()}] Failed to send status: {str(e)}")
    
    async def send_transcription(self, session_id: str, text: str):
        """Send transcribed text to frontend for display"""
        if session_id in self.active_connections:
            message = json.dumps({
                "type": "transcription",
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.warning(f"Failed to send transcription: {str(e)}")

manager = ConnectionManager()

@router.websocket("/ws/session/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    logger.info(f"[{datetime.now().isoformat()}] WebSocket connection initiated for session: {session_id}")
    await manager.connect(websocket, session_id)
    
    # Verify session exists
    async with async_session() as db:
        session = await db.get(Session, session_id)
        if not session:
            logger.warning(f"[{datetime.now().isoformat()}] Session not found: {session_id}")
            await websocket.close(code=4004, reason="Session not found")
            return
        
        schema = await db.get(Schema, session.schema_id)
        logger.info(f"[{datetime.now().isoformat()}] Session verified, schema fields: {schema.fields}")
    
    try:
        await manager.send_status(session_id, "ready", "Connected and ready for audio/text")
        logger.info(f"[{datetime.now().isoformat()}] WebSocket ready, waiting for data...")
        
        packet_count = 0
        while True:
            # Receive raw message and handle both text and binary
            ws_msg = await websocket.receive()
            packet_count += 1
            
            if ws_msg["type"] == "websocket.disconnect":
                logger.info(f"[{datetime.now().isoformat()}] Client disconnected")
                break
            
            # Handle text messages (JSON)
            if "text" in ws_msg:
                data = ws_msg["text"]
                logger.info(f"\n{'='*80}")
                logger.info(f"[{datetime.now().isoformat()}] PACKET #{packet_count} RECEIVED!")
                logger.info(f"Session ID: {session_id}")
                logger.info(f"Raw text data length: {len(data)} bytes")
                
                message = json.loads(data)
            # Handle binary data
            elif "bytes" in ws_msg:
                audio_bytes = ws_msg["bytes"]
                logger.info(f"\n{'='*80}")
                logger.info(f"[{datetime.now().isoformat()}] PACKET #{packet_count} RECEIVED!")
                logger.info(f"Session ID: {session_id}")
                logger.info(f"Binary audio data: {len(audio_bytes)} bytes")
                logger.info(f"Processing binary audio chunk...")
                
                # Convert to base64 for existing process_audio_chunk function
                import base64
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                await process_audio_chunk(session_id, audio_base64, schema.fields)
                logger.info(f"{'='*80}\n")
                continue
            else:
                logger.warning(f"Unexpected message format: {ws_msg.keys()}")
                continue
            
            # Log parsed message details
            logger.info(f"Message type: {message.get('type', 'UNKNOWN')}")
            if message["type"] == "audio_chunk":
                audio_data_len = len(message.get("data", ""))
                logger.info(f"Audio data (base64) length: {audio_data_len} chars")
                logger.info(f"Estimated audio size: ~{audio_data_len * 3 / 4:.0f} bytes")
                logger.info(f"Processing audio chunk...")
                await process_audio_chunk(session_id, message["data"], schema.fields)
            elif message["type"] == "text_chunk":
                text_data = message.get("data", "")
                logger.info(f"Text data: '{text_data}'")
                logger.info(f"Processing text chunk...")
                await process_text_chunk(session_id, message["data"], schema.fields)
            elif message["type"] == "stop_recording":
                logger.info(f"Stop recording signal received")
                await manager.send_status(session_id, "stopped", "Recording stopped")
            else:
                logger.warning(f"Unknown message type: {message.get('type')}")
            
            logger.info(f"{'='*80}\n")
                
    except WebSocketDisconnect:
        logger.info(f"[{datetime.now().isoformat()}] WebSocket disconnected for session: {session_id}")
        manager.disconnect(websocket, session_id)
    except Exception as e:
        logger.error(f"[{datetime.now().isoformat()}] WebSocket error for session {session_id}: {str(e)}", exc_info=True)
        manager.disconnect(websocket, session_id)

async def process_audio_chunk(session_id: str, audio_data: str, fields: List[str]):
    """Process audio chunk through transcription and intelligent agent"""
    logger.info(f"[{datetime.now().isoformat()}] Starting audio processing for session: {session_id}")
    await manager.send_status(session_id, "processing", "Processing audio...")
    
    # Decode base64 audio data from frontend
    try:
        audio_bytes = base64.b64decode(audio_data)
        logger.info(f"[{datetime.now().isoformat()}] Decoded audio size: {len(audio_bytes)} bytes")
    except Exception as e:
        logger.error(f"[{datetime.now().isoformat()}] Failed to decode audio: {str(e)}")
        await manager.send_status(session_id, "error", f"Invalid audio data: {str(e)}")
        return
    
    # Transcribe audio using Groq Whisper
    transcription_service = GroqTranscriptionService()
    text = await transcription_service.transcribe_audio_chunk(audio_bytes)
    
    if not text:
        logger.info(f"⚠️ No speech detected in audio")
        await manager.send_status(session_id, "ready", "No speech detected")
        return
    
    logger.info(f"🎤 TRANSCRIPTION: '{text}'")
    
    # Send transcription to frontend for display
    await manager.send_transcription(session_id, text)
    
    # Get conversation memory from Mem0
    mem0_service = Mem0MemoryService()
    context = await mem0_service.get_relevant_context(text, str(session_id))
    
    # Run intelligent agent
    intelligent_extractor = IntelligentExtractor()
    result = intelligent_extractor.forward(text, fields, context)
    
    # Log agent action
    action = result['action_type']
    if action == ActionType.EXTRACT_FIELDS.value:
        logger.info(f"🤖 AGENT ACTION: Extract Fields - {result.get('extracted_fields', {})}")
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
            
            # Send real-time update to frontend
            logger.info(f"✅ FIELD UPDATE: {field} = '{field_value}'")
            await manager.send_field_update(session_id, field, field_value)
            
            # Save to database
            async with async_session() as db:
                # Check if field already exists for this session
                existing_data = await db.execute(
                    select(SessionData).where(
                        SessionData.session_id == session_id
                    )
                )
                session_data_list = existing_data.scalars().all()
                
                # Update existing or create new
                found = False
                for sd in session_data_list:
                    if field in sd.data:
                        sd.data[field] = field_value
                        found = True
                        break
                
                if not found:
                    # Create new session data record
                    new_data = {field: field_value}
                    session_data = SessionData(
                        session_id=session_id,
                        data=new_data
                    )
                    db.add(session_data)
                
                await db.commit()
            
    elif result["action_type"] == ActionType.STORE_CONTEXT.value:
        # Store context only in memory
        await mem0_service.add_conversation_memory(
            text=text,
            session_id=str(session_id),
            action_taken=result["action_type"],
            extracted_fields={}
        )
        await manager.send_status(session_id, "ready", "Context stored for future reference")
    else:
        # Ignored - not relevant to form filling
        await manager.send_status(session_id, "ready", "Audio processed")

async def process_text_chunk(session_id: str, text: str, fields: List[str]):
    """Process text through intelligent agent and send immediate field updates"""
    # Send the text input as transcription for consistency
    await manager.send_transcription(session_id, text)
    
    # Get conversation memory from Mem0
    mem0_service = Mem0MemoryService()
    context = await mem0_service.get_relevant_context(text, str(session_id))
    
    # Run intelligent agent
    intelligent_extractor = IntelligentExtractor()
    result = intelligent_extractor.forward(text, fields, context)
    
    # Log agent action
    action = result['action_type']
    if action == ActionType.EXTRACT_FIELDS.value:
        logger.info(f"🤖 AGENT ACTION: Extract Fields - {result.get('extracted_fields', {})}")
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
        
        # Send each field update immediately to React frontend
        for field, field_value in result["extracted_fields"].items():
            # Store field in memory
            await mem0_service.update_field_memory(
                session_id=str(session_id),
                field_name=field,
                field_value=field_value
            )
            
            # Send real-time update to frontend with high confidence
            await manager.send_field_update(session_id, field, field_value)
            
            # Save to database
            async with async_session() as db:
                # Check if field already exists for this session
                existing_data = await db.execute(
                    select(SessionData).where(
                        SessionData.session_id == session_id
                    )
                )
                session_data_list = existing_data.scalars().all()
                
                # Update existing or create new
                found = False
                for sd in session_data_list:
                    if field in sd.data:
                        sd.data[field] = field_value
                        found = True
                        break
                
                if not found:
                    # Create new session data record
                    new_data = {field: field_value}
                    session_data = SessionData(
                        session_id=session_id,
                        data=new_data
                    )
                    db.add(session_data)
                
                await db.commit()
    
    elif result["action_type"] == ActionType.STORE_CONTEXT.value:
        # Store context only in memory
        await mem0_service.add_conversation_memory(
            text=text,
            session_id=str(session_id),
            action_taken=result["action_type"],
            extracted_fields={}
        )
        await manager.send_status(session_id, "ready", "Context stored for future reference")
    else:
        # Ignored - not relevant to form filling
        await manager.send_status(session_id, "ready", "Text processed")