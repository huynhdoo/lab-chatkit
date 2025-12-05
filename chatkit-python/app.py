"""
Combined FastAPI and FastHTML application.

Run both the backend API and frontend UI in a single process.
"""

import asyncio
import threading
import uvicorn
from main import app as api_app
from frontend import app as frontend_app
from fastapi.middleware.cors import CORSMiddleware


def run_api():
    """Run the FastAPI backend on port 8000."""
    config = uvicorn.Config(
        api_app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


def run_frontend():
    """Run the FastHTML frontend on port 3000."""
    # Add CORS to FastHTML app if needed
    from fasthtml.common import serve
    serve(frontend_app, port=3000)


if __name__ == "__main__":
    print("Starting ChatKit application...")
    print("Backend API: http://localhost:8000")
    print("Frontend UI: http://localhost:3000")
    print("API Docs: http://localhost:8000/docs")
    
    # Run frontend on main thread
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\nShutting down...")
