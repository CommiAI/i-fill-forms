import httpx
import tempfile
import os
import logging
from typing import Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class GroqTranscriptionService:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "whisper-large-v3-turbo"  # Fast Groq Whisper model
    
    async def transcribe_audio_chunk(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio chunk using Groq Whisper API."""
        try:
            # Detect audio format
            mime_type = 'audio/webm'
            suffix = '.webm'
            
            # Check for WAV header (RIFF)
            if len(audio_data) >= 4 and audio_data[:4] == b'RIFF':
                mime_type = 'audio/wav'
                suffix = '.wav'
            # Check for WebM header
            elif len(audio_data) >= 4 and audio_data[:4] == b'\x1a\x45\xdf\xa3':
                mime_type = 'audio/webm'
                suffix = '.webm'
            
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Send to Groq API
            async with httpx.AsyncClient(timeout=30.0) as client:
                with open(temp_file_path, 'rb') as audio_file:
                    files = {'file': (f'audio{suffix}', audio_file, mime_type)}
                    data = {
                        'model': self.model,
                        'response_format': 'text'
                    }
                    headers = {'Authorization': f'Bearer {self.api_key}'}
                    
                    response = await client.post(
                        f"{self.base_url}/audio/transcriptions",
                        files=files,
                        data=data,
                        headers=headers
                    )
            
            # Cleanup temp file
            os.unlink(temp_file_path)
            
            if response.status_code == 200:
                transcription = response.text.strip()
                if transcription:
                    return transcription
                else:
                    logger.info("⚠️ Empty transcription received from Groq")
                    return None
            else:
                logger.error(f"❌ Groq API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Transcription error: {e}")
            # Cleanup temp file if it exists
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return None