# Setup AutoJobApply from GitHub

This guide helps you set up the AutoJobApply project after cloning from GitHub.

## Prerequisites

- Python 3.9+
- Node.js 16+
- Git

## Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/stillalive04/Auto_appliER_V2.git
cd Auto_appliER_V2
```

### 2. Run Automated Setup
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Start the Application
```bash
./start_app.sh
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Manual Setup (if automated setup fails)

### Backend Setup
```bash
# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start backend server
python main.py
```

### Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start frontend development server
npm run dev
```

## Important Notes

⚠️ **Virtual Environment**: The `.venv` folder is excluded from the repository (916MB). You must create it locally using the setup instructions above.

⚠️ **Dependencies**: All Python packages must be installed in your local virtual environment. The `requirements.txt` file contains all necessary dependencies.

⚠️ **Node Modules**: The `node_modules` folder is also excluded and will be created when you run `npm install`.

## Features

- **Real Job Scraping**: Live job listings from LinkedIn, Indeed, Glassdoor, Handshake
- **AI Resume Enhancement**: Automatic skill upgrades based on job requirements
- **AI Cover Letter Generation**: Personalized cover letters for each application
- **Multi-Platform Support**: US and Canada job markets
- **Automated Applications**: Submit applications across multiple platforms

## Troubleshooting

### Common Issues

1. **Port already in use**: Kill existing processes on ports 8000 and 5173
2. **Python dependencies missing**: Ensure virtual environment is activated
3. **Node modules missing**: Run `npm install` in the frontend directory

### Getting Help

1. Check the logs: `tail -f backend.log` and `tail -f frontend.log`
2. Ensure all dependencies are installed
3. Verify Python and Node.js versions

## Development

- Backend runs on FastAPI with live job scraping
- Frontend built with React + TypeScript + Vite + Tailwind CSS
- Real-time job data from major platforms
- AI-powered resume and cover letter generation 