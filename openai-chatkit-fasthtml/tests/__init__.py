"""Tests for session management."""

import pytest
from unittest.mock import patch, AsyncMock
from app.session import (
    create_chatkit_session,
    create_or_get_session_cookie,
    build_session_cookie_header,
    extract_upstream_error,
)


@pytest.mark.asyncio
async def test_create_chatkit_session_success():
    """Test successful session creation."""
    mock_response = {
        "token": "test-token",
        "session_id": "test-session",
    }
    
    with patch("app.session.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.post.return_value = AsyncMock()
        mock_instance.post.return_value.json.return_value = mock_response
        mock_instance.post.return_value.raise_for_status = AsyncMock()
        
        mock_client.return_value = mock_instance
        
        result = await create_chatkit_session(
            api_key="test-key",
            workflow_id="wf_test",
        )
        
        assert result == mock_response


@pytest.mark.asyncio
async def test_create_chatkit_session_missing_api_key():
    """Test session creation with missing API key."""
    with pytest.raises(ValueError, match="Missing OPENAI_API_KEY"):
        await create_chatkit_session(
            api_key="",
            workflow_id="wf_test",
        )


@pytest.mark.asyncio
async def test_create_or_get_session_cookie():
    """Test session cookie creation."""
    headers = {}
    user_id, session_cookie = await create_or_get_session_cookie(headers)
    
    assert user_id
    assert session_cookie
    assert len(user_id) == 32  # hex(16)
    assert len(session_cookie) == 64  # hex(32)


def test_extract_upstream_error():
    """Test error extraction from upstream response."""
    # Test with error dict
    result = extract_upstream_error({"error": {"message": "Test error"}})
    assert result == "Test error"
    
    # Test with error string
    result = extract_upstream_error({"error": "Simple error"})
    assert result == "Simple error"
    
    # Test with None
    result = extract_upstream_error(None)
    assert result == "Unknown error"


def test_build_session_cookie_header():
    """Test session cookie header building."""
    header = build_session_cookie_header("test-cookie")
    
    assert "test-cookie" in header
    assert "Path=/" in header
    assert "HttpOnly" in header
    assert "SameSite=Lax" in header
