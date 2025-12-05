# ChatKit FastAPI + FastHTML - Quick Start Guide

A minimal, production-ready chatbot application combining FastAPI backend and FastHTML frontend.

## What You Get

✅ **FastAPI Backend** - REST API for chat operations  
✅ **FastHTML Frontend** - Clean, responsive chat UI  
✅ **OpenAI Integration** - ChatKit workflow support  
✅ **Session Management** - Track conversations  
✅ **Auto-documentation** - Swagger UI at `/docs`  

## 5-Minute Setup

### 1. Install & Configure (2 min)
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key and workflow ID
```

### 2. Run (30 seconds)
```bash
./start.sh
```

### 3. Chat (open browser)
- **UI**: http://localhost:5001
- **API Docs**: http://localhost:8000/docs

## Files Overview

| File | Purpose |
|------|---------|
| `main.py` | FastAPI backend (port 8000) |
| `frontend.py` | FastHTML frontend (port 5001) |
| `start.sh` | Run both servers together |
| `.env` | Configuration (API keys, workflow ID) |

## Key Features

### Backend API
- `POST /api/create-session` - Create chat session
- `POST /api/chat` - Send message and get response
- `GET /health` - Health check

### Frontend UI
- Clean gradient design
- Real-time message updates with HTMX
- Loading indicators
- Error handling
- Responsive mobile support

## Environment Variables

```env
OPENAI_API_KEY=sk_...              # Required: Your OpenAI API key
CHATKIT_WORKFLOW_ID=wf_...         # Required: Your workflow ID
CHATKIT_API_BASE=https://api.openai.com  # Optional
API_BASE_URL=http://localhost:8000 # Optional: Frontend API endpoint
```

## Development

### Run backend only:
```bash
python main.py
```

### Run frontend only:
```bash
python frontend.py
```

### View API documentation:
Visit http://localhost:8000/docs in your browser

## Architecture

```
┌─────────────────────┐
│  FastHTML Frontend  │ Port 5001
│   (Chat UI)         │
└──────────┬──────────┘
           │
         HTTPS
           │
┌──────────▼──────────┐
│   FastAPI Backend   │ Port 8000
│  (Chat API)         │
└──────────┬──────────┘
           │
         HTTPS
           │
┌──────────▼──────────┐
│   OpenAI ChatKit    │
│   (Workflow)        │
└─────────────────────┘
```

## Common Issues

**"OPENAI_API_KEY environment variable is required"**
- Make sure `.env` file exists with valid API key

**Frontend can't reach API**
- Verify `API_BASE_URL` in `.env` matches backend location
- Backend must be running on http://localhost:8000

**Port already in use**
- Backend: Change port 8000 in `main.py`
- Frontend: Change port 5001 in `frontend.py`

## Next Steps

- Customize chat UI in `frontend.py` (styles, layout)
- Add database for conversation history
- Deploy to production (Railway, Render, etc.)
- Add authentication/user management
- Integrate with your own backend

## References

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [FastHTML Docs](https://www.fastht.ml/docs/)
- [OpenAI ChatKit](https://openai.github.io/chatkit-python/)
- [HTMX Docs](https://htmx.org/)
