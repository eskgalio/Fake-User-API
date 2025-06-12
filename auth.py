from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
from datetime import datetime, timedelta
import secrets
import json
from pathlib import Path

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
API_KEYS_FILE = "api_keys.json"

class APIKeyManager:
    def __init__(self):
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self):
        """Load API keys from file or create new if doesn't exist."""
        if Path(API_KEYS_FILE).exists():
            with open(API_KEYS_FILE, 'r') as f:
                return json.load(f)
        return {}

    def _save_api_keys(self):
        """Save API keys to file."""
        with open(API_KEYS_FILE, 'w') as f:
            json.dump(self.api_keys, f, indent=2)

    def create_api_key(self, name: str, tier: str = "free") -> str:
        """Create a new API key."""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            "name": name,
            "tier": tier,
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "calls_count": 0
        }
        self._save_api_keys()
        return api_key

    def validate_api_key(self, api_key: str) -> bool:
        """Validate an API key and update usage statistics."""
        if api_key in self.api_keys:
            self.api_keys[api_key]["last_used"] = datetime.now().isoformat()
            self.api_keys[api_key]["calls_count"] += 1
            self._save_api_keys()
            return True
        return False

    def get_key_info(self, api_key: str) -> Optional[dict]:
        """Get information about an API key."""
        return self.api_keys.get(api_key)

api_key_manager = APIKeyManager()

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Verify API key middleware."""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    if not api_key_manager.validate_api_key(api_key):
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key 