#!/bin/bash

# Combined starter script for ChatKit FastAPI + FastHTML

echo "🚀 Starting ChatKit Application..."
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:5001"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
python main.py &
BACKEND_PID=$!

# Give backend time to start
sleep 2

# Start frontend in foreground (so Ctrl+C works)
python frontend.py &
FRONTEND_PID=$!

# Wait for both processes
wait
