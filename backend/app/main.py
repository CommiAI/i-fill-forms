from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.api import schemas, sessions, websocket, export, audio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown

app = FastAPI(
    title="I-Fill-Forms API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (will be uncommented as we implement them)
app.include_router(schemas.router, prefix="/api/schemas", tags=["schemas"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(websocket.router, tags=["websocket"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}