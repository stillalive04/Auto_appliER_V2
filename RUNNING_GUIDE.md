# 🚀 AutoJobApply - Running Guide

This guide will help you set up and run the AutoJobApply application on your local machine.

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+** - [Download from python.org](https://python.org)
- **Node.js 16+** - [Download from nodejs.org](https://nodejs.org)
- **npm** (comes with Node.js)

## 🛠️ Quick Setup

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Start the full application:**
   ```bash
   ./run_app.sh
   ```

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   # Create and activate virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Install Frontend dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Run the application:**
   ```bash
   # Option A: Run both together
   ./run_app.sh
   
   # Option B: Run separately
   ./run_backend.sh    # In terminal 1
   ./run_frontend.sh   # In terminal 2
   ```

## 🎯 Application URLs

Once running, you can access:

- **🌐 Frontend:** http://localhost:5173
- **🔧 Backend API:** http://localhost:8000
- **📚 API Documentation:** http://localhost:8000/docs
- **🗄️ Database Debug:** http://localhost:8000/debug/database

## 🔧 Individual Components

### Backend Only
```bash
./run_backend.sh
```
- Starts FastAPI server on port 8000
- Includes auto-reload for development
- API documentation available at `/docs`

### Frontend Only
```bash
./run_frontend.sh
```
- Starts Vite development server
- Usually runs on port 5173 (or next available)
- Hot module replacement enabled

### Database
The application uses an **in-memory database** for development:
- No separate database server needed
- Data is reset when backend restarts
- View current data at: http://localhost:8000/debug/database

## 📊 Features Available

### Core Features
- ✅ User Registration & Authentication
- ✅ Resume Upload & Management
- ✅ Job Preferences Configuration
- ✅ Automated Job Applications
- ✅ Real-time Notifications
- ✅ Application Analytics

### Advanced Features
- ✅ County-level Job Scraping (3,144+ counties)
- ✅ CAPTCHA Solving Capabilities
- ✅ Real Company Name Extraction
- ✅ Experience Levels (Internship to C-Suite)
- ✅ Comprehensive Job Types (W2, C2H, 1099, Contract, etc.)
- ✅ Custom AI Integration (DeepSeek & Gemini)

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes on specific ports
   lsof -Pi :8000 -sTCP:LISTEN -t | xargs kill -9  # Backend
   lsof -Pi :5173 -sTCP:LISTEN -t | xargs kill -9  # Frontend
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall Python dependencies
   source .venv/bin/activate
   pip install -r requirements.txt
   
   # Reinstall Frontend dependencies
   cd frontend && npm install
   ```

3. **Virtual Environment Issues**
   ```bash
   # Recreate virtual environment
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Backend Won't Start**
   ```bash
   # Check logs
   tail -f backend.log
   
   # Manual start for debugging
   cd backend
   source ../.venv/bin/activate
   python main.py
   ```

5. **Frontend Won't Start**
   ```bash
   # Check logs
   tail -f frontend.log
   
   # Manual start for debugging
   cd frontend
   npm run dev
   ```

### Environment Variables

The application uses the following environment variables (optional):

```bash
# AI Service API Keys (set in your environment)
export DEEPSEEK_API_KEY="your_deepseek_api_key"
export GEMINI_API_KEY="your_gemini_api_key"

# Database Configuration (for future use)
export DATABASE_URL="sqlite:///./autojobapply.db"
```

## 📝 Development Notes

### File Structure
```
auto_apply/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application file
│   ├── ai_services/        # AI integration services
│   ├── automation/         # Job automation logic
│   └── notifications/      # Notification system
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/         # React pages
│   │   └── components/    # React components
│   └── package.json
├── requirements.txt        # Python dependencies
├── setup.sh               # Setup script
├── run_backend.sh         # Backend runner
├── run_frontend.sh        # Frontend runner
└── run_app.sh            # Full app runner
```

### Development Workflow
1. Make changes to code
2. Backend auto-reloads (if using `--reload`)
3. Frontend hot-reloads automatically
4. Check logs in `backend.log` and `frontend.log`

### API Testing
- Use the interactive API docs at http://localhost:8000/docs
- Test endpoints with curl or Postman
- View database state at `/debug/database`

## 🚀 Production Deployment

For production deployment, consider:

1. **Use a proper database** (PostgreSQL, MySQL)
2. **Set up environment variables** for API keys
3. **Use a production WSGI server** (Gunicorn)
4. **Build the frontend** for production
5. **Set up reverse proxy** (Nginx)
6. **Configure SSL/TLS** certificates

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs (`backend.log`, `frontend.log`)
3. Ensure all prerequisites are installed
4. Try the manual setup process

## 🎉 Success!

If everything is working correctly, you should see:
- Frontend loading at http://localhost:5173
- Backend API responding at http://localhost:8000
- Ability to register/login users
- Job automation features available

Happy job hunting! 🎯 