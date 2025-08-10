import tempfile
import os
import logging
import asyncio
from typing import Optional
from groq import Groq
from app.config.settings import settings

logger = logging.getLogger(__name__)

class GroqTranscriptionService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "whisper-large-v3-turbo"  # Fast Groq Whisper model
    
    async def transcribe_audio_chunk(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio chunk using Groq Whisper API."""
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Use Groq SDK to transcribe - run in executor since it's synchronous
            loop = asyncio.get_event_loop()
            
            def transcribe_sync():
                with open(temp_file_path, 'rb') as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        file=audio_file,
                        model=self.model,
                        response_format="text",
                        temperature=0.0
                    )
                    return transcription
            
            # Run the synchronous SDK call in an executor
            transcription = await loop.run_in_executor(None, transcribe_sync)
            
            # Cleanup temp file
            os.unlink(temp_file_path)
            
            if transcription:
                return transcription
            else:
                return None
                
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            # Cleanup temp file if it exists
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return None