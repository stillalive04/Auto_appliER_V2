#!/bin/bash

echo "🎨 Starting AutoJobApply Frontend..."

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed. Please run ./setup.sh first"
    exit 1
fi

# Kill any existing process on common frontend ports
echo "🔄 Checking for existing processes on frontend ports..."
for port in 5173 5174 5175 5176 3000; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is in use. Killing existing process..."
        kill -9 $(lsof -Pi :$port -sTCP:LISTEN -t)
        sleep 1
    fi
done

# Change to frontend directory and start development server
cd frontend
echo "🌐 Starting Vite development server..."
echo "🎯 Frontend will be available at: http://localhost:5173"
echo "🔗 Make sure backend is running at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the development server
npm run dev 