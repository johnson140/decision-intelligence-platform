"""
Pydantic models for API request/response validation.
These define what data looks like when traveling through the API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HealthResponse(BaseModel):
    """Response for health check endpoint"""
    status: str
    message: str
    timestamp: datetime


class UploadResponse(BaseModel):
    """Response after uploading data"""
    success: bool
    message: str
    records_processed: int