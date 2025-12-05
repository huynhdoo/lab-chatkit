"""
Minimal FastHTML frontend for ChatKit FastAPI chatbot.

A simple web UI for interacting with the FastAPI chat API.
"""

from fasthtml.common import *
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Create FastHTML app with custom headers for HTMX
app, rt = fast_app(
    title="ChatKit Bot",
    pico=False,  # We'll use custom CSS instead
)

# Styling
style = Style("""
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .container {
        width: 100%;
        max-width: 600px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        height: 90vh;
        max-height: 800px;
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px 12px 0 0;
        text-align: center;
    }
    
    .header h1 {
        font-size: 24px;
        margin-bottom: 5px;
    }
    
    .header p {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        background-color: #f8f9fa;
    }
    
    .message {
        display: flex;
        gap: 10px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message.user {
        justify-content: flex-end;
    }
    
    .message-content {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        line-height: 1.4;
    }
    
    .message.user .message-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .message.assistant .message-content {
        background: #e9ecef;
        color: #333;
        border-bottom-left-radius: 4px;
    }
    
    .message.error .message-content {
        background: #f8d7da;
        color: #721c24;
        border-left: 4px solid #f5c6cb;
    }
    
    .input-area {
        padding: 20px;
        border-top: 1px solid #e9ecef;
        display: flex;
        gap: 10px;
    }
    
    .input-area form {
        display: flex;
        gap: 10px;
        width: 100%;
    }
    
    .input-area input {
        flex: 1;
        padding: 12px 16px;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        font-size: 14px;
        transition: border-color 0.3s;
    }
    
    .input-area input:focus {
        outline: none;
        border-color: #667eea;
    }
    
    .input-area button {
        padding: 12px 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .input-area button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .input-area button:active {
        transform: translateY(0);
    }
    
    .loading {
        display: flex;
        gap: 4px;
        align-items: center;
        padding: 12px 16px;
    }
    
    .loading span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: bounce 1.4s infinite;
    }
    
    .loading span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .loading span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes bounce {
        0%, 80%, 100% {
            opacity: 0.3;
        }
        40% {
            opacity: 1;
        }
    }
    
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #999;
        text-align: center;
    }
    
    .empty-state p {
        font-size: 16px;
        margin-bottom: 10px;
    }
    
    .empty-state small {
        font-size: 12px;
    }
""")


# Components
def message_bubble(content: str, is_user: bool = True, is_error: bool = False):
    """Create a message bubble."""
    msg_class = "user" if is_user else ("error" if is_error else "assistant")
    return Div(
        Div(content, cls="message-content"),
        cls=f"message {msg_class}",
        id=f"msg-{hash(content)}"
    )


def loading_indicator():
    """Create a loading indicator."""
    return Div(
        Span(), Span(), Span(),
        cls="loading"
    )


def chat_interface():
    """Create the main chat interface."""
    return Div(
        # Header
        Div(
            H1("ChatKit Bot"),
            P("Powered by OpenAI ChatKit API"),
            cls="header"
        ),
        
        # Messages container
        Div(
            Div(
                P("👋 Welcome to ChatKit!"),
                P(Small("Start a conversation by typing a message below")),
                cls="empty-state",
                id="empty-state"
            ),
            cls="chat-messages",
            id="messages"
        ),
        
        # Input area
        Div(
            Form(
                Input(
                    type="text",
                    name="message",
                    placeholder="Ask me anything...",
                    autocomplete="off"
                ),
                Button("Send", type="submit"),
                hx_post="/send",
                hx_target="#messages",
                hx_swap="beforeend",
                onsubmit="if(!this.message.value.trim()) return false; "
                        "document.getElementById('empty-state').style.display='none';"
            ),
            cls="input-area"
        ),
        
        cls="container"
    )


@app.get("/")
def index():
    """Main page."""
    return Html(
        Head(
            Title("ChatKit FastHTML Bot"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
            style,
        ),
        Body(
            chat_interface(),
        )
    )


@rt("/send", methods=["post"])
def send_message(message: str):
    """Handle incoming messages."""
    if not message or not message.strip():
        return ""
    
    # Show user message immediately
    user_msg = message_bubble(message, is_user=True)
    
    # Create a placeholder for the assistant message
    assistant_placeholder = Div(
        loading_indicator(),
        cls="message assistant",
        id="assistant-msg"
    )
    
    # Return both messages
    return Fragment(
        user_msg,
        Script(f"""
            (function() {{
                const input = document.querySelector('input[name="message"]');
                input.value = '';
                input.focus();
                
                // Fetch response from API
                fetch('{API_BASE_URL}/api/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        message: '{message}',
                        session_id: 'default-session',
                        user_id: null
                    }})
                }})
                .then(r => r.json())
                .then(data => {{
                    const placeholder = document.getElementById('assistant-msg');
                    if (placeholder) {{
                        placeholder.innerHTML = `<div class="message-content">${{data.response}}</div>`;
                    }}
                    // Auto-scroll to bottom
                    const messagesDiv = document.getElementById('messages');
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }})
                .catch(err => {{
                    const placeholder = document.getElementById('assistant-msg');
                    if (placeholder) {{
                        placeholder.innerHTML = `<div class="message-content" style="background: #f8d7da; color: #721c24; border-left: 4px solid #f5c6cb;">Error: ${{err.message}}</div>`;
                    }}
                }});
            }})();
        """),
        assistant_placeholder,
    )


@rt("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    serve()
