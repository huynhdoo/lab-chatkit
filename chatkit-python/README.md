# ChatKit FastAPI Minimal Chatbot

A minimal FastAPI application that integrates with OpenAI's ChatKit to create a simple chatbot REST API.

## Features

- **Session Management**: Create and manage chat sessions
- **Chat Endpoint**: Send messages and receive AI-powered responses
- **CORS Support**: Ready for frontend integration
- **Health Checks**: Built-in health check endpoint
- **Auto-documentation**: Automatic API documentation via Swagger UI

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

### 3. Run the Application

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 4. Test the API

Visit the interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```
GET /health
```

Returns server status.

### Create Session
```
POST /api/create-session
Content-Type: application/json

{
  "user_id": "user123",
  "metadata": {}
}
```

Returns a session ID for managing conversations.

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

Returns the AI response to your message.

## Project Structure

```
chatkit-python/
├── main.py              # FastAPI application and routes
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Configuration

The application uses environment variables from `.env`:

- `OPENAI_API_KEY` (required): Your OpenAI API key from https://platform.openai.com/api-keys
- `CHATKIT_WORKFLOW_ID` (required): Your workflow ID from Agent Builder (e.g., `wf_...`)
- `CHATKIT_API_BASE` (optional): Defaults to `https://api.openai.com`

## Development

For local development with auto-reload:

```bash
python main.py
```

The app runs in reload mode by default, watching for file changes.

## Production

For production deployment, modify the `uvicorn.run()` call in `main.py`:

```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=False  # Disable auto-reload in production
)
```

Or use:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI ChatKit Documentation](https://openai.github.io/chatkit-python/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## License

MIT
