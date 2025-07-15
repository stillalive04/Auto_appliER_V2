#!/bin/bash

echo "🚀 Starting AutoJobApply Backend..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if we're in the correct directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: backend/main.py not found"
    exit 1
fi

# Kill any existing process on port 8000
echo "🔄 Checking for existing processes on port 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8000 is in use. Killing existing process..."
    kill -9 $(lsof -Pi :8000 -sTCP:LISTEN -t)
    sleep 2
fi

# Change to backend directory and start server
cd backend
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📊 API Documentation: http://localhost:8000/docs"
echo "🗄️  Database Debug: http://localhost:8000/debug/database"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 