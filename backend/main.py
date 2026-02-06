"""
Decision Intelligence Platform - FastAPI Backend
Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from core.config import settings
from core.models import HealthResponse

# Create the FastAPI application
app = FastAPI(
    title="Decision Intelligence Platform",
    description="A decision-first platform for transactional businesses",
    version="1.0.0"
)

# Add CORS middleware 
# frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - confirms the API is running"""
    return HealthResponse(
        status="operational",
        message="Decision Intelligence Platform API",
        timestamp=datetime.now()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="All systems operational",
        timestamp=datetime.now()
    )