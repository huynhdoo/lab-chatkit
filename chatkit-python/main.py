"""
Minimal FastAPI chatbot application using OpenAI ChatKit.

This application provides REST endpoints for:
- Creating ChatKit sessions
- Sending messages and receiving responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ChatKit FastAPI Bot",
    description="A minimal FastAPI chatbot using OpenAI ChatKit",
    version="1.0.0"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHATKIT_WORKFLOW_ID = os.getenv("CHATKIT_WORKFLOW_ID")
CHATKIT_API_BASE = os.getenv("CHATKIT_API_BASE", "https://api.openai.com")


def get_openai_client():
    """Initialize OpenAI client (lazy initialization to avoid httpx conflicts)."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=OPENAI_API_KEY, base_url=CHATKIT_API_BASE)


# Request/Response models
class CreateSessionRequest(BaseModel):
    user_id: str | None = None
    metadata: dict | None = None


class CreateSessionResponse(BaseModel):
    session_id: str
    user_id: str | None = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: str
    user_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/create-session", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    """
    Create a new ChatKit session.
    
    This endpoint initializes a session for ChatKit workflow interactions.
    """
    try:
        # Generate a session ID (in production, use a UUID)
        import uuid
        session_id = str(uuid.uuid4())
        
        return CreateSessionResponse(
            session_id=session_id,
            user_id=request.user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get a response using ChatKit workflow.
    
    This endpoint sends a user message through the ChatKit workflow
    and returns the assistant's response.
    """
    try:
        # Create a completion using the ChatKit workflow
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",  # ChatKit typically uses gpt-4
            messages=[
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        # Extract the response content
        assistant_message = response.choices[0].message.content
        
        return ChatResponse(
            response=assistant_message,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "message": "Welcome to ChatKit FastAPI Bot",
        "docs": "/docs",
        "workflow_id": CHATKIT_WORKFLOW_ID,
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the app with: python main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
