# ChatKit FastAPI Minimal Chatbot

A minimal FastAPI application with FastHTML frontend that integrates with OpenAI's ChatKit to create a simple chatbot.

## Features

- **FastAPI Backend**: REST API for chat operations with session management
- **FastHTML Frontend**: Minimal, responsive web UI for chatting
- **Session Management**: Create and manage chat sessions
- **CORS Support**: Ready for frontend integration
- **Auto-documentation**: Automatic API documentation via Swagger UI at `/docs`
- **Real-time Chat**: Live message streaming with loading indicators

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
- `OPENAI_API_KEY`: Your OpenAI API key
- `CHATKIT_WORKFLOW_ID`: Your ChatKit workflow ID (starts with `wf_`)
- `CHATKIT_API_BASE`: (Optional) Custom ChatKit API base URL
- `API_BASE_URL`: (Optional) Frontend API base URL (defaults to `http://localhost:8000`)

### 3. Run the Application

**Option A: Run Everything Together**
```bash
./start.sh
```
Opens both backend and frontend automatically.

**Option B: Run Frontend Only** (if backend is running elsewhere)
```bash
python frontend.py
```
Visit `http://localhost:5001` (FastHTML default port)

**Option C: Run Backend Only** (For API testing)
```bash
python main.py
```
API available at `http://localhost:8000`
Swagger UI: `http://localhost:8000/docs`

**Option D: Run Both Separately** (in different terminals)
```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Start frontend
python frontend.py
```

Then visit `http://localhost:5001` for the UI and `http://localhost:8000/docs` for API docs.

## Project Structure

```
chatkit-python/
├── main.py              # FastAPI backend application
├── frontend.py          # FastHTML frontend application
├── start.sh             # Startup script to run both servers
├── app.py               # Combined app runner (optional)
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Architecture

### Backend (`main.py`)
- FastAPI REST API on port 8000
- OpenAI ChatKit integration
- Session management
- CORS-enabled

### Frontend (`frontend.py`)
- FastHTML web UI on port 3000
- Responsive chat interface
- HTMX-powered interactions
- Real-time message streaming

## API Endpoints

### Health Check
```
GET /health
```

### Create Session
```
POST /api/create-session
Content-Type: application/json

{
  "user_id": "user123",
  "metadata": {}
}
```

### Send Message
```
POST /api/chat
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "session-uuid",
  "user_id": "user123"
}
```

## Configuration

The application uses environment variables from `.env`:

- `OPENAI_API_KEY` (required): Your OpenAI API key from https://platform.openai.com/api-keys
- `CHATKIT_WORKFLOW_ID` (required): Your workflow ID from Agent Builder (e.g., `wf_...`)
- `CHATKIT_API_BASE` (optional): Defaults to `https://api.openai.com`
- `API_BASE_URL` (optional): Backend API base URL for frontend (defaults to `http://localhost:8000`)

## Frontend Features

- **Clean Chat Interface**: Modern gradient design with smooth animations
- **Message Bubbles**: Distinct styling for user and assistant messages
- **Loading States**: Visual feedback while waiting for responses
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on desktop and mobile devices
- **HTMX Integration**: Fast, interactive updates without page reloads

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastHTML Documentation](https://www.fastht.ml/docs/)
- [OpenAI ChatKit Documentation](https://openai.github.io/chatkit-python/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [HTMX Documentation](https://htmx.org/)

## License

MIT
