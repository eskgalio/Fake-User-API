from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum

class UserTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class ExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    XML = "xml"

class UserBase(BaseModel):
    """Base user model with extended fields."""
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    address: str = Field(..., min_length=5)
    phone: str
    job: str
    birthdate: Optional[date] = None
    company: Optional[str] = None
    username: Optional[str] = None
    website: Optional[HttpUrl] = None
    # Additional fields
    avatar_url: Optional[HttpUrl] = None
    social_media: Optional[Dict[str, str]] = None
    skills: Optional[List[str]] = None
    education: Optional[List[Dict[str, Any]]] = None
    languages: Optional[List[str]] = None
    credit_card: Optional[Dict[str, str]] = None

class UserResponse(BaseModel):
    """Single user response model."""
    success: bool = True
    data: UserBase
    request_id: str
    timestamp: str

class UsersResponse(BaseModel):
    """Multiple users response model."""
    success: bool = True
    count: int
    data: List[UserBase]
    request_id: str
    timestamp: str
    page: Optional[int] = None
    total_pages: Optional[int] = None

class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    error_code: str
    request_id: str
    timestamp: str

class APIKeyResponse(BaseModel):
    """API key response model."""
    api_key: str
    name: str
    tier: UserTier
    created_at: str
    rate_limit: int

class APIKeyRequest(BaseModel):
    """API key request model."""
    name: str = Field(..., min_length=3, max_length=50)
    tier: UserTier = UserTier.FREE

class ExportRequest(BaseModel):
    """Data export request model."""
    format: ExportFormat = ExportFormat.JSON
    count: int = Field(..., gt=0, le=1000)
    include_fields: Optional[List[str]] = None 