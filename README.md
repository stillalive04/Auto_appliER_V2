# AutoJobApply - Intelligent Job Application Automation

AutoJobApply is a comprehensive full-stack web application that automates job applications across major platforms including LinkedIn, Indeed, Glassdoor, Handshake, and newspaper job postings across Canada and USA. The system uses advanced AI to optimize resumes and generate personalized cover letters for each application.

## 🚀 Features

### Core Functionality
- **Multi-Platform Job Scraping**: Automatically finds jobs from LinkedIn, Indeed, and newspaper sources
- **AI-Powered Resume Enhancement**: Uses DeepSeek API to optimize resumes for specific job postings
- **Intelligent Cover Letter Generation**: Uses Gemini API to create personalized cover letters
- **Automated Application Process**: Applies to jobs automatically with rate limiting to avoid detection
- **Real-time Analytics**: Track application success rates, responses, and performance metrics
- **Beautiful 3D UI**: Modern interface with realistic mountain backgrounds and parallax effects

### AI Integration
- **DeepSeek API**: Advanced resume optimization and keyword integration
- **Gemini API**: Personalized cover letter generation with company-specific content
- **Smart Matching**: Calculates job-resume compatibility scores
- **ATS Optimization**: Ensures resumes and cover letters are ATS-friendly

### Automation Features
- **Background Processing**: Runs automation sessions in the background
- **Rate Limiting**: 5-second delays between applications to avoid detection
- **Session Management**: Track active automation sessions and their progress
- **Error Handling**: Robust error handling with detailed logging
- **Manual Fallback**: Newspaper jobs flagged for manual follow-up

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.13
- **Database**: In-memory database (easily replaceable with MongoDB)
- **AI Services**: DeepSeek and Gemini API integration
- **Authentication**: Secure password hashing with bcrypt
- **File Upload**: Support for PDF, DOC, DOCX, and TXT resumes
- **Background Tasks**: Async job processing with FastAPI BackgroundTasks

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development
- **Styling**: Tailwind CSS with custom 3D animations
- **State Management**: React hooks and local storage
- **Routing**: React Router for navigation
- **UI Features**: 3D mountain backgrounds, parallax effects, modal dialogs

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

The backend will be available at `http://127.0.0.1:8000`

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5176` (or next available port)

## 🔧 Configuration

### API Keys
The system uses the following APIs (already configured):
- **DeepSeek API**: For resume enhancement
- **Gemini API**: For cover letter generation

### Environment Variables
Create a `.env` file in the backend directory:
```env
DEEPSEEK_API_KEY=your_deepseek_key
GEMINI_API_KEY=your_gemini_key
```

## 📖 Usage

### 1. User Registration
- Visit the frontend URL
- Click "Get Started Free" on the home page
- Fill in registration details
- Login with your credentials

### 2. Upload Resume
- Navigate to the Dashboard
- Click "Upload Resume"
- Select your resume file (PDF, DOC, DOCX, or TXT)
- The system will store and process your resume

### 3. Set Job Preferences
- Click "Set Job Preferences" on the dashboard
- Configure:
  - Job titles you're interested in
  - Preferred locations
  - Salary range
  - Experience level
  - Maximum applications per session

### 4. Start Automation
- Click "Start Auto-Apply" to begin automated job applications
- The system will:
  - Search for relevant jobs
  - Enhance your resume for each job
  - Generate personalized cover letters
  - Apply to jobs automatically
  - Track application results

### 5. Monitor Progress
- View real-time analytics on the dashboard
- Track application success rates
- Monitor active automation sessions
- Review recent application activity

## 🎯 Dashboard Features

### Statistics Cards
- **Applications Sent**: Total number of applications submitted
- **Success Rate**: Percentage of successful applications
- **Active Sessions**: Currently running automation sessions

### Quick Actions
- **Upload Resume**: ✅ Status indicator shows if resume is uploaded
- **Set Job Preferences**: ⚠️ Status indicator shows if preferences are set
- **Start Auto-Apply**: Disabled until resume and preferences are set
- **View Analytics**: Detailed performance metrics

### Recent Activity
- Real-time feed of recent applications
- Success/failure indicators
- Company and job title information
- Application timestamps

## 🤖 AI Services

### Resume Enhancement (DeepSeek API)
- Analyzes job descriptions for keywords
- Optimizes resume content for ATS systems
- Maintains truthfulness while improving relevance
- Provides match scores and improvement summaries

### Cover Letter Generation (Gemini API)
- Creates personalized cover letters for each job
- Incorporates company-specific information
- Uses professional tone and structure
- Optimizes for ATS compatibility

## 🔒 Security Features

- **Password Hashing**: Secure bcrypt hashing for user passwords
- **API Rate Limiting**: Prevents abuse of automation features
- **Input Validation**: Comprehensive validation of all user inputs
- **Error Handling**: Secure error messages without sensitive data exposure

## 📊 Analytics & Monitoring

### Application Tracking
- Success/failure rates
- Response tracking
- Platform performance comparison
- Time-based analytics

### Session Management
- Active automation sessions
- Session progress tracking
- Error logging and reporting
- Performance metrics

## 🌐 Supported Platforms

### Currently Active
- ✅ **LinkedIn**: Easy Apply jobs
- ✅ **Indeed**: Direct applications
- ✅ **Newspapers**: Canadian and US job postings (flagged for manual follow-up)

### Planned Support
- 🔄 **Glassdoor**: Company reviews and jobs
- 🔄 **Handshake**: University career services
- 🔄 **Monster**: Job search platform
- 🔄 **CareerBuilder**: Professional networking

## 🚨 Rate Limiting & Ethics

The system implements responsible automation:
- **5-second delays** between applications
- **Respectful scraping** with proper headers
- **Manual fallback** for newspaper jobs
- **Error handling** to avoid overwhelming servers

## 🎨 UI/UX Features

### 3D Mountain Backgrounds
- Realistic mountain silhouettes with CSS clip-path
- Parallax effects based on mouse movement
- Animated stars and floating clouds
- Aurora-like gradient effects

### Interactive Elements
- Hover effects with 3D transformations
- Glass morphism design with backdrop blur
- Smooth animations and transitions
- Responsive design for all screen sizes

## 📝 API Documentation

### Authentication Endpoints
- `POST /register` - User registration
- `POST /login` - User authentication

### Job Management
- `POST /upload-resume` - Upload resume file
- `POST /set-job-preferences` - Set job search criteria
- `POST /start-automation` - Begin automated applications
- `GET /automation-status/{session_id}` - Check automation progress

### Analytics
- `GET /user-analytics/{user_id}` - Get user statistics
- `GET /user-profile/{user_id}` - Get user profile
- `GET /job-platforms` - List supported platforms

## 🔧 Development

### Backend Structure
```
backend/
├── main.py                 # FastAPI application
├── automation/
│   ├── job_automation.py   # Main automation engine
│   ├── job_scraper.py      # Job scraping logic
│   ├── job_applier.py      # Application submission
│   └── newspaper_scraper.py # Newspaper job scraping
├── ai_services/
│   ├── resume_enhancer.py  # DeepSeek integration
│   └── cover_letter_generator.py # Gemini integration
├── database.py             # In-memory database
└── requirements.txt        # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.tsx        # Landing page
│   │   ├── Register.tsx    # User registration
│   │   ├── Login.tsx       # User login
│   │   └── Dashboard.tsx   # Main dashboard
│   ├── components/         # Reusable components
│   └── main.tsx           # Application entry point
├── package.json           # Node.js dependencies
└── vite.config.ts         # Vite configuration
```

## 🚀 Deployment

### Production Considerations
- Replace in-memory database with MongoDB
- Add proper environment variable management
- Implement proper logging and monitoring
- Add API rate limiting middleware
- Use production-grade web servers (Gunicorn, Nginx)

### Docker Support
```dockerfile
# Backend Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 📞 Support

For issues or questions:
1. Check the console logs for detailed error messages
2. Verify API keys are properly configured
3. Ensure all dependencies are installed
4. Check that both backend and frontend are running

## 🏆 Success Metrics

The system is designed to:
- **Apply to 1,000+ jobs** automatically
- **Achieve 60%+ application success rate**
- **Generate personalized content** for each application
- **Maintain ethical scraping practices**
- **Provide comprehensive analytics**

## 🎯 Future Enhancements

- **Mobile App**: React Native mobile application
- **Email Integration**: Automated email responses
- **Interview Scheduling**: Calendar integration
- **Salary Negotiation**: AI-powered salary advice
- **Network Analysis**: LinkedIn connection optimization

---

**AutoJobApply** - Revolutionizing job search through intelligent automation and AI-powered personalization. # Auto_appliER_V2
