"""Session management and API utilities for ChatKit."""

import json
import logging
import secrets
from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

import httpx
from pydantic import BaseModel, Field

from .config import ChatKitConfig


logger = logging.getLogger(__name__)


class CreateSessionRequest(BaseModel):
    """Request body for creating a ChatKit session."""
    workflow: Optional[dict[str, str]] = None
    scope: Optional[dict[str, str]] = None
    chatkit_configuration: Optional[dict[str, Any]] = None


class SessionResponse(BaseModel):
    """Response from ChatKit session creation."""
    token: str
    session_id: str
    expires_at: datetime


async def create_chatkit_session(
    api_key: str,
    workflow_id: str,
    user_id: Optional[str] = None,
    file_upload_enabled: bool = False,
    api_base: str = "https://api.openai.com",
) -> dict[str, Any]:
    """Create a ChatKit session via OpenAI API.
    
    Args:
        api_key: OpenAI API key
        workflow_id: ChatKit workflow ID
        user_id: Optional user ID for session scope
        file_upload_enabled: Whether file uploads are enabled
        api_base: Base URL for ChatKit API
        
    Returns:
        Response from ChatKit API
        
    Raises:
        httpx.HTTPError: If the API request fails
        ValueError: If required parameters are missing
    """
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")
    
    if not workflow_id:
        raise ValueError("Missing workflow_id")
    
    url = f"{api_base}/v1/chatkit/sessions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "chatkit_beta=v1",
    }
    
    payload = {
        "workflow": {"id": workflow_id},
        "chatkit_configuration": {
            "file_upload": {
                "enabled": file_upload_enabled,
            },
        },
    }
    
    if user_id:
        payload["user"] = user_id
    
    logger.debug(f"Creating ChatKit session for workflow: {workflow_id}")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


async def create_or_get_session_cookie(
    request_headers: dict[str, str],
) -> tuple[str, Optional[str]]:
    """Create or get an existing session cookie.
    
    Args:
        request_headers: HTTP request headers (for cookie extraction)
        
    Returns:
        Tuple of (user_id, session_cookie)
    """
    # Extract existing session cookie if present
    cookie_header = request_headers.get("cookie", "")
    session_cookie = None
    
    for cookie in cookie_header.split(";"):
        if ChatKitConfig.SESSION_COOKIE_NAME in cookie:
            session_cookie = cookie.split("=", 1)[1].strip()
            break
    
    # Generate new user ID if no session exists
    user_id = secrets.token_hex(16)
    
    # Create new session cookie if not present
    if not session_cookie:
        session_cookie = secrets.token_hex(32)
    
    return user_id, session_cookie


def build_session_cookie_header(
    session_cookie: str,
) -> str:
    """Build Set-Cookie header value.
    
    Args:
        session_cookie: Session cookie value
        
    Returns:
        Cookie header value
    """
    max_age = ChatKitConfig.SESSION_COOKIE_MAX_AGE
    expires = datetime.utcnow() + timedelta(seconds=max_age)
    expires_str = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    return (
        f"{ChatKitConfig.SESSION_COOKIE_NAME}={session_cookie}; "
        f"Path=/; "
        f"Max-Age={max_age}; "
        f"Expires={expires_str}; "
        f"HttpOnly; "
        f"SameSite=Lax"
    )


def extract_upstream_error(response_data: Optional[dict[str, Any]]) -> str:
    """Extract error message from ChatKit API response.
    
    Args:
        response_data: Response JSON from ChatKit API
        
    Returns:
        Error message string
    """
    if not response_data:
        return "Unknown error"
    
    if "error" in response_data:
        error = response_data["error"]
        if isinstance(error, dict):
            return error.get("message", str(error))
        return str(error)
    
    return str(response_data)
