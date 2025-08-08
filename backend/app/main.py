"""Main FastAPI application for I-Fill-Forms hackathon."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "I-Fill-Forms API is running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# TODO: Add your API routes here
# from app.api import pdf, websocket
# app.include_router(pdf.router, prefix="/api/pdf", tags=["pdf"])
# app.include_router(websocket.router, prefix="/ws", tags=["websocket"])