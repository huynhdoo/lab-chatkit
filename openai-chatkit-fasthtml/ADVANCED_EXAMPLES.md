# Exemples avancés

Ce document fournit des exemples d'utilisation avancée du projet ChatKit FastHTML.

## 1. Ajouter une authentification utilisateur

### Avec JWT

```python
# app/auth.py
import jwt
from datetime import datetime, timedelta
from functools import wraps
from fasthtml.common import Request, Response

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")

def create_jwt_token(user_id: str) -> str:
    """Create a JWT token for a user."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def require_auth(func):
    """Decorator to require JWT authentication."""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not token:
            return json_resp({"error": "Unauthorized"}, status_code=401)
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user_id = payload["user_id"]
        except jwt.InvalidTokenError:
            return json_resp({"error": "Invalid token"}, status_code=401)
        
        return await func(request, *args, **kwargs)
    
    return wrapper

# app/routes.py
@app.post("/api/create-session")
@require_auth
async def create_session_auth(request: Request) -> Response:
    """Create session with user authentication."""
    user_id = request.state.user_id
    # ... reste de la logique
```

## 2. Ajouter Redis pour la gestion des sessions

```python
# app/session.py
import redis.asyncio as redis
from typing import Optional

class SessionManager:
    """Manage sessions with Redis."""
    
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis_url = redis_url
        self._redis: Optional[redis.Redis] = None
    
    async def get_redis(self) -> redis.Redis:
        """Get Redis connection."""
        if not self._redis:
            self._redis = await redis.from_url(self.redis_url)
        return self._redis
    
    async def store_session(self, session_id: str, token: str, ttl: int = 86400):
        """Store session in Redis."""
        r = await self.get_redis()
        await r.setex(session_id, ttl, token)
    
    async def get_session(self, session_id: str) -> Optional[str]:
        """Get session from Redis."""
        r = await self.get_redis()
        return await r.get(session_id)

# Usage
session_manager = SessionManager()

@app.post("/api/create-session")
async def create_session(request: Request) -> Response:
    session = await create_chatkit_session(...)
    await session_manager.store_session(
        session_cookie,
        session["token"],
        ttl=30*24*3600  # 30 days
    )
    return json_resp(session)
```

## 3. Ajouter WebSocket pour le streaming

```python
# app/websocket.py
from fasthtml.common import WebSocket

@app.websocket("/ws/stream")
async def stream_chat(websocket: WebSocket):
    """Stream chat responses via WebSocket."""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Appeler OpenAI avec streaming
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "https://api.openai.com/v1/chat/completions",
                    json=data,
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = json.loads(line[6:])
                            await websocket.send_json(chunk)
    
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
```

## 4. Ajouter Analytics

```python
# app/analytics.py
from datetime import datetime

class AnalyticsTracker:
    """Track user interactions."""
    
    async def track_session_created(self, user_id: str, workflow_id: str):
        """Track session creation."""
        event = {
            "event": "session_created",
            "user_id": user_id,
            "workflow_id": workflow_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        # Send to analytics service
        await self.send_to_service(event)
    
    async def track_message(self, user_id: str, message: str, role: str):
        """Track user message."""
        event = {
            "event": "message",
            "user_id": user_id,
            "message": message,
            "role": role,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.send_to_service(event)
    
    async def send_to_service(self, event: dict):
        """Send event to analytics service."""
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://analytics.example.com/events",
                json=event,
            )

analytics = AnalyticsTracker()

@app.post("/api/create-session")
async def create_session(request: Request) -> Response:
    # ... existing code
    await analytics.track_session_created(user_id, workflow_id)
    return json_resp(session)
```

## 5. Ajouter une file d'attente de tâches avec Celery

```python
# app/tasks.py
from celery import Celery
import os

celery_app = Celery(
    "chatkit",
    broker=os.getenv("REDIS_URL", "redis://localhost"),
    backend=os.getenv("REDIS_URL", "redis://localhost"),
)

@celery_app.task
def process_user_message(user_id: str, message: str, session_token: str):
    """Process message asynchronously."""
    # Call OpenAI API
    # Save to database
    # Send notifications
    pass

# app/routes.py
@app.post("/api/messages")
async def handle_message(request: Request) -> Response:
    """Handle user message."""
    data = await request.json()
    
    # Queue task
    process_user_message.delay(
        user_id=data.get("user_id"),
        message=data.get("message"),
        session_token=data.get("session_token"),
    )
    
    return json_resp({"status": "processing"})
```

## 6. Ajouter une base de données

```python
# app/db.py
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    message_count = Column(Integer, default=0)

class ChatSession(Base):
    """Chat session model."""
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    token = Column(String)
    workflow_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        yield session

# app/routes.py
@app.post("/api/create-session")
async def create_session(request: Request, db: AsyncSession = Depends(get_db)) -> Response:
    # ... create session
    
    # Save to database
    session_record = ChatSession(
        id=session_cookie,
        user_id=user_id,
        token=session["token"],
        workflow_id=workflow_id,
    )
    db.add(session_record)
    await db.commit()
    
    return json_resp(session)
```

## 7. Ajouter les notifications par email

```python
# app/notifications.py
import aiosmtplib
from email.mime.text import MIMEText

async def send_email(to: str, subject: str, html: str):
    """Send email notification."""
    message = MIMEText(html, "html")
    message["Subject"] = subject
    message["From"] = os.getenv("SMTP_FROM_EMAIL")
    message["To"] = to
    
    async with aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587) as smtp:
        await smtp.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD"),
        )
        await smtp.send_message(message)

async def notify_session_created(user_email: str, session_id: str):
    """Notify user of session creation."""
    await send_email(
        to=user_email,
        subject="ChatKit Session Created",
        html=f"""
        <h1>Welcome to ChatKit!</h1>
        <p>Your session has been created successfully.</p>
        <p>Session ID: {session_id}</p>
        """,
    )
```

## 8. Ajouter un système de cache

```python
# app/cache.py
import aiocache
from aiocache import cached, Cache

@cached(cache=Cache.MEMORY, ttl=3600)
async def get_workflow_config(workflow_id: str) -> dict:
    """Get and cache workflow configuration."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.openai.com/v1/workflows/{workflow_id}",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        )
        return response.json()

# Usage
config = await get_workflow_config(workflow_id)
```

## 9. Ajouter des tests d'intégration

```python
# tests/test_integration.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_session_integration():
    """Test session creation end-to-end."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/create-session",
            json={
                "workflow": {"id": "wf_test"},
                "chatkit_configuration": {"file_upload": {"enabled": False}},
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "session_id" in data

@pytest.mark.asyncio
async def test_get_home_page():
    """Test home page loads."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        
        assert response.status_code == 200
        assert "chatkit" in response.text.lower()
```

## 10. Ajouter le monitoring avec Prometheus

```python
# app/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

session_creations = Counter(
    "chatkit_sessions_created",
    "Number of sessions created",
    ["workflow_id"],
)

session_duration = Histogram(
    "chatkit_session_duration_seconds",
    "Session duration in seconds",
)

active_sessions = Gauge(
    "chatkit_active_sessions",
    "Number of active sessions",
)

@app.post("/api/create-session")
async def create_session(request: Request) -> Response:
    start_time = time.time()
    
    try:
        # ... create session
        session_creations.labels(workflow_id=workflow_id).inc()
        active_sessions.inc()
        return json_resp(session)
    finally:
        duration = time.time() - start_time
        session_duration.observe(duration)

# app/main.py
from prometheus_client import make_asgi_app
from starlette.routing import Mount

app.router.routes.append(
    Mount("/metrics", app=make_asgi_app())
)
```

## 11. Ajouter la traduction (i18n)

```python
# app/i18n.py
from enum import Enum

class Language(str, Enum):
    EN = "en"
    FR = "fr"
    ES = "es"

TRANSLATIONS = {
    "greeting": {
        Language.EN: "How can I help you today?",
        Language.FR: "Comment puis-je vous aider aujourd'hui?",
        Language.ES: "¿Cómo puedo ayudarte hoy?",
    },
}

def get_text(key: str, lang: Language = Language.EN) -> str:
    """Get translated text."""
    return TRANSLATIONS.get(key, {}).get(lang, key)

# app/routes.py
@app.get("/api/config")
async def config(request: Request) -> Response:
    lang = request.query_params.get("lang", "en")
    language = Language(lang)
    
    return json_resp({
        "greeting": get_text("greeting", language),
        # ...
    })
```

## 12. Ajouter le rate limiting

```python
# app/middleware.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# app/main.py
app = FastHTML(debug=DEBUG)
limiter.init_app(app)

@app.post("/api/create-session")
@limiter.limit("5/minute")
async def create_session(request: Request) -> Response:
    # ... existing code
    return json_resp(session)
```

Ces exemples montrent comment étendre l'application de base avec des fonctionnalités avancées!
