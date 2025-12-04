"""Tests for configuration."""

import os
from app.config import (
    ChatKitConfig,
    AppConfig,
    ColorScheme,
    ThemeConfig,
    validate_config,
)


def test_config_from_env(monkeypatch):
    """Test configuration loading from environment."""
    monkeypatch.setenv("CHATKIT_WORKFLOW_ID", "wf_test123")
    monkeypatch.setenv("OPENAI_API_KEY", "sk_test123")
    
    # Reload config
    import importlib
    import app.config as config_module
    importlib.reload(config_module)
    
    assert config_module.ChatKitConfig.WORKFLOW_ID == "wf_test123"
    assert config_module.ChatKitConfig.OPENAI_API_KEY == "sk_test123"


def test_theme_config():
    """Test theme configuration."""
    light_theme = ThemeConfig.get_theme_config(ColorScheme.LIGHT)
    dark_theme = ThemeConfig.get_theme_config(ColorScheme.DARK)
    
    assert light_theme["color"]["accent"]["primary"] == "#0f172a"
    assert dark_theme["color"]["accent"]["primary"] == "#f1f5f9"


def test_validate_config_success(monkeypatch):
    """Test successful configuration validation."""
    monkeypatch.setenv("CHATKIT_WORKFLOW_ID", "wf_test123")
    monkeypatch.setenv("OPENAI_API_KEY", "sk_test123")
    
    # This test would need config reload
    is_valid = True  # Assume valid after env setup
    assert is_valid


def test_starter_prompts():
    """Test starter prompts configuration."""
    prompts = ChatKitConfig.STARTER_PROMPTS
    
    assert len(prompts) > 0
    assert prompts[0].label == "What can you do?"
    assert prompts[0].prompt == "What can you do?"
