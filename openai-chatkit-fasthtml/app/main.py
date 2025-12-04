"""Main FastHTML application for ChatKit."""

import logging
import sys
from pathlib import Path

from fasthtml.common import (
    FastHTML,
    Request,
    Response,
    Html,
    Head,
    Body,
    Div,
    Script,
    Link,
    Meta,
    Title,
    Button,
    Span,
)
import uvicorn

from .config import AppConfig, ChatKitConfig, validate_config
from .routes import handle_create_session, handle_health_check, handle_config


# Configure logging
logging.basicConfig(
    level=logging.DEBUG if AppConfig.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Validate configuration on startup
is_valid, error_msg = validate_config()
if not is_valid:
    logger.error(f"Configuration error: {error_msg}")
    if not AppConfig.DEBUG:
        sys.exit(1)

# Create FastHTML app
app = FastHTML(
    debug=AppConfig.DEBUG,
    title="ChatKit Starter",
    static_path="static",
)


# Route: GET /
@app.get("/")
def home(request: Request) -> Html:
    """Serve the main ChatKit page.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        HTML page with ChatKit component
    """
    return Html(
        Head(
            Meta(charset="utf-8"),
            Meta(
                name="viewport",
                content="width=device-width, initial-scale=1",
            ),
            Title("ChatKit - OpenAI"),
            Link(rel="stylesheet", href="/static/styles.css"),
            Meta(name="color-scheme", content="light dark"),
        ),
        Body(
            Div(
                # Header
                Div(
                    cls="header",
                    id="header",
                    children=[
                        Div(
                            cls="container",
                            children=[
                                Span(
                                    "ChatKit",
                                    style="font-size: 1.5rem; font-weight: 600;",
                                ),
                                Button(
                                    "🌓",
                                    id="theme-toggle",
                                    cls="theme-toggle",
                                    title="Toggle dark mode",
                                ),
                            ],
                            style="display: flex; justify-content: space-between; align-items: center;",
                        ),
                    ],
                ),
                # Main content
                Div(
                    cls="main",
                    children=[
                        # ChatKit container
                        Div(
                            id="chatkit-container",
                            cls="chatkit-container loading",
                            children=[
                                Div(
                                    cls="spinner",
                                ),
                            ],
                        ),
                        # Error overlay
                        Div(
                            id="error-overlay",
                            cls="error-overlay",
                            style="display: none;",
                            children=[
                                Div(
                                    cls="error-overlay-content",
                                    children=[
                                        Div(
                                            "Error",
                                            cls="error-overlay-title",
                                        ),
                                        Div(
                                            id="error-message",
                                            cls="error-overlay-message",
                                        ),
                                        Button(
                                            "Retry",
                                            id="retry-button",
                                            cls="error-overlay-button",
                                            onclick="window.retryChatKit && window.retryChatKit()",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                cls="main-wrapper",
                style="display: flex; flex-direction: column; height: 100vh;",
            ),
            # Load ChatKit web component
            Script(src="https://chatkit.openai.com/assets/chatkit.js", defer=True),
            # Load ChatKit initialization script
            Script(
                src="/static/chatkit.js",
                defer=True,
                data_workflow_id=ChatKitConfig.WORKFLOW_ID,
                data_session_endpoint=AppConfig.CREATE_SESSION_ENDPOINT,
                data_placeholder=ChatKitConfig.PLACEHOLDER_INPUT,
                data_greeting=ChatKitConfig.GREETING,
            ),
        ),
    )


# Route: POST /api/create-session
@app.post("/api/create-session")
async def create_session(request: Request) -> Response:
    """Create a ChatKit session.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        JSON response with session token
    """
    return await handle_create_session(request)


# Route: GET /api/health
@app.get("/api/health")
async def health(request: Request) -> Response:
    """Health check endpoint.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        JSON response with health status
    """
    return await handle_health_check(request)


# Route: GET /api/config
@app.get("/api/config")
async def config(request: Request) -> Response:
    """Get client configuration.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        JSON response with configuration
    """
    return await handle_config(request)


def run():
    """Run the FastHTML application."""
    logger.info(
        f"Starting ChatKit FastHTML server on {AppConfig.HOST}:{AppConfig.PORT}"
    )
    
    uvicorn.run(
        app,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=AppConfig.DEBUG,
        log_level="debug" if AppConfig.DEBUG else "info",
    )


if __name__ == "__main__":
    run()
