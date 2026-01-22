"""
Decision Intelligence Platform - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import decisions, data_ingestion
from core.config import settings

app = FastAPI(
    title="Decision Intelligence Platform",
    description="A decision-first platform for transactional businesses",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data_ingestion.router, prefix="/api/v1", tags=["Data Ingestion"])
app.include_router(decisions.router, prefix="/api/v1", tags=["Decisions"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Decision Intelligence Platform API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
