#!/bin/bash

echo "🚀 Starting AutoJobApply Application..."

# Check if setup has been run
if [ ! -d ".venv" ] || [ ! -d "frontend/node_modules" ]; then
    echo "🔧 Running initial setup..."
    ./setup.sh
fi

# Start the application
echo "🌟 Starting both backend and frontend..."
./run_app.sh 