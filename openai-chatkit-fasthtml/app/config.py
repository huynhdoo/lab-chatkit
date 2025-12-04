"""Configuration management for ChatKit FastHTML app."""

import os
from typing import Optional
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class ColorScheme(str, Enum):
    """Theme color scheme."""
    LIGHT = "light"
    DARK = "dark"


@dataclass
class StarterPrompt:
    """A starter prompt for the chat interface."""
    label: str
    prompt: str
    icon: str = "circle-question"


class ChatKitConfig:
    """OpenAI ChatKit configuration."""
    
    WORKFLOW_ID: str = os.getenv("CHATKIT_WORKFLOW_ID", "").strip()
    API_BASE: str = os.getenv("CHATKIT_API_BASE", "https://api.openai.com")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # ChatKit UI Configuration
    STARTER_PROMPTS: list[StarterPrompt] = [
        StarterPrompt(
            label="What can you do?",
            prompt="What can you do?",
            icon="circle-question",
        ),
    ]
    
    PLACEHOLDER_INPUT: str = "Ask anything..."
    GREETING: str = "How can I help you today?"
    
    # Session management
    SESSION_COOKIE_NAME: str = "chatkit_session_id"
    SESSION_COOKIE_MAX_AGE: int = 60 * 60 * 24 * 30  # 30 days


class AppConfig:
    """Application configuration."""
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    CREATE_SESSION_ENDPOINT: str = "/api/create-session"


class ThemeConfig:
    """Theme configuration for different color schemes."""
    
    @staticmethod
    def get_theme_config(scheme: ColorScheme) -> dict:
        """Get theme configuration for the given color scheme."""
        return {
            "color": {
                "grayscale": {
                    "hue": 220,
                    "tint": 6,
                    "shade": -1 if scheme == ColorScheme.DARK else -4,
                },
                "accent": {
                    "primary": "#f1f5f9" if scheme == ColorScheme.DARK else "#0f172a",
                    "level": 1,
                },
            },
            "radius": "round",
        }


def validate_config() -> tuple[bool, Optional[str]]:
    """Validate required configuration.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not ChatKitConfig.WORKFLOW_ID:
        return False, "Missing CHATKIT_WORKFLOW_ID environment variable"
    
    if not ChatKitConfig.OPENAI_API_KEY:
        return False, "Missing OPENAI_API_KEY environment variable"
    
    return True, None
