from fastapi import FastAPI, HTTPException, Path, Query, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Optional, List
import uvicorn
import uuid
from datetime import datetime
import time
from collections import defaultdict
from typing import Dict, Tuple

from config import get_settings
from schemas import (
    UserResponse, UsersResponse, ErrorResponse, APIKeyResponse,
    APIKeyRequest, ExportRequest, UserTier
)
from services import UserGenerator
from auth import verify_api_key, api_key_manager

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory rate limiter
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = defaultdict(list)
        
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        key_requests = self.requests[key]
        
        # Remove old requests
        while key_requests and key_requests[0] < now - window:
            key_requests.pop(0)
            
        # Check if under limit
        if len(key_requests) < limit:
            key_requests.append(now)
            return True
        return False

rate_limiter = RateLimiter()

# Create a global UserGenerator instance
user_generator = UserGenerator()

def get_request_id():
    """Generate a unique request ID."""
    return str(uuid.uuid4())

def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def check_rate_limit(api_key: str, limit: int, window: int = 60):
    """Check rate limit for the given API key."""
    if not rate_limiter.is_allowed(api_key, limit, window):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": get_timestamp(),
        "version": settings.APP_VERSION
    }

@app.post("/api-keys", response_model=APIKeyResponse, tags=["API Keys"])
async def create_api_key(request: APIKeyRequest):
    """Create a new API key."""
    api_key = api_key_manager.create_api_key(request.name, request.tier)
    return APIKeyResponse(
        api_key=api_key,
        name=request.name,
        tier=request.tier,
        created_at=datetime.utcnow().isoformat(),
        rate_limit=100 if request.tier == UserTier.FREE else 1000
    )

@app.get("/user", response_model=UserResponse, tags=["Users"])
async def get_user(api_key: str = Depends(verify_api_key)):
    """Get a single fake user."""
    check_rate_limit(api_key, 100)
    try:
        user_data = user_generator.generate_user()
        return UserResponse(
            data=user_data,
            request_id=get_request_id(),
            timestamp=get_timestamp()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e), "error_code": "GENERATION_FAILED"}
        )

@app.get("/users/{count}", response_model=UsersResponse, tags=["Users"])
async def get_users(
    count: int = Path(..., gt=0, le=settings.MAX_USERS_PER_REQUEST),
    country: Optional[str] = Query(None, min_length=2, max_length=5),
    page: Optional[int] = Query(None, gt=0),
    page_size: Optional[int] = Query(None, gt=0, le=50),
    api_key: str = Depends(verify_api_key)
):
    """Get multiple fake users with pagination support."""
    check_rate_limit(api_key, 50)
    try:
        if country:
            users = user_generator.generate_users_by_country(country, count)
        else:
            users = user_generator.generate_users(count)

        # Handle pagination
        if page and page_size:
            start = (page - 1) * page_size
            end = start + page_size
            users = users[start:end]
            total_pages = (count + page_size - 1) // page_size
        else:
            total_pages = None

        return UsersResponse(
            count=len(users),
            data=users,
            request_id=get_request_id(),
            timestamp=get_timestamp(),
            page=page,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e), "error_code": "GENERATION_FAILED"}
        )

@app.post("/export", tags=["Export"])
async def export_users(
    request: ExportRequest,
    api_key: str = Depends(verify_api_key)
):
    """Export users in specified format."""
    check_rate_limit(api_key, 10)
    try:
        users = user_generator.generate_users(request.count)
        content = user_generator.export_users(
            users,
            request.format,
            request.include_fields
        )
        
        media_types = {
            "json": "application/json",
            "csv": "text/csv",
            "xml": "application/xml"
        }
        
        return Response(
            content=content,
            media_type=media_types[request.format],
            headers={
                "Content-Disposition": f"attachment; filename=users.{request.format}",
                "X-Request-ID": get_request_id()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e), "error_code": "EXPORT_FAILED"}
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 