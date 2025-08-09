from mem0 import Memory
from typing import List, Dict, Optional
import os
import asyncio
from app.config.settings import settings

class Mem0MemoryService:
    def __init__(self):
        """Initialize Mem0 memory with configuration."""
        self.config = {
            "llm": {
                "provider": "groq",
                "config": {
                    "model": "openai/gpt-oss-120b",
                    "temperature": 0.1,
                    "api_key": settings.groq_api_key
                }
            },
            "embedder": {
                "provider": "openai", 
                "config": {
                    "model": "text-embedding-3-small",
                    "api_key": settings.openai_api_key
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "form_conversations",
                    "host": "localhost",
                    "port": 6333
                }
            }
        }
        self.memory = Memory.from_config(self.config)
    
    async def add_conversation_memory(self, 
                                    text: str, 
                                    session_id: str, 
                                    action_taken: str,
                                    extracted_fields: Dict = None) -> str:
        """Store conversation interaction in Mem0."""
        messages = [
            {
                "role": "user", 
                "content": f"User said: {text}"
            },
            {
                "role": "assistant", 
                "content": f"Action taken: {action_taken}. Fields extracted: {extracted_fields or {}}"
            }
        ]
        
        # Store with session-scoped memory
        result = await asyncio.to_thread(
            self.memory.add,
            messages=messages,
            user_id=session_id,
            metadata={
                "action": action_taken,
                "extracted_fields": extracted_fields or {},
                "interaction_type": "form_filling"
            }
        )
        return result
    
    async def get_relevant_context(self, 
                                 query: str, 
                                 session_id: str, 
                                 limit: int = 5) -> str:
        """Retrieve relevant memories for current interaction."""
        search_results = await asyncio.to_thread(
            self.memory.search,
            query=query,
            user_id=session_id,
            limit=limit
        )
        
        if not search_results or "results" not in search_results:
            return ""
        
        # Format memories into context string
        context_parts = []
        for result in search_results["results"]:
            memory_text = result.get("memory", "")
            context_parts.append(f"Previous: {memory_text}")
        
        return "\n".join(context_parts)
    
    async def update_field_memory(self, 
                                session_id: str, 
                                field_name: str, 
                                field_value: str):
        """Store field extraction as persistent memory."""
        message = f"User's {field_name} is {field_value}"
        
        result = await asyncio.to_thread(
            self.memory.add,
            messages=[{"role": "system", "content": message}],
            user_id=session_id,
            metadata={
                "field_name": field_name,
                "field_value": field_value,
                "memory_type": "field_extraction"
            }
        )
        return result