# Blood Test Analyzer

A FastAPI-based application that uses Google Gemini AI to analyze blood test reports and provide comprehensive health insights. This project combines AI-powered analysis with medical knowledge to help users understand their blood test results.

## 🏆 Bonus Features Implemented

### 🚀 **Queue Worker Model (Redis + Celery)**
- **Concurrent Request Handling**: Processes multiple blood test analyses simultaneously
- **Background Processing**: Non-blocking API responses with task queuing
- **Scalable Architecture**: Can handle high load with multiple workers
- **Task Monitoring**: Real-time status tracking for each analysis
- **Automatic Cleanup**: Background tasks for data maintenance

### 🗄️ **Database Integration (SQLAlchemy)**
- **Persistent Storage**: All analysis results stored in database
- **User Management**: Ready for future user authentication
- **Analysis History**: Complete audit trail of all processed reports
- **Performance Metrics**: Processing time and file size tracking
- **Data Cleanup**: Automatic removal of old records

### 📊 **Enhanced API Endpoints**
- `POST /analyze` - Queue analysis request (non-blocking)
- `GET /status/{analysis_id}` - Check analysis progress and results
- `GET /analyses` - List all analyses with filtering
- `DELETE /analyses/{analysis_id}` - Remove analysis records
- `GET /health` - Comprehensive system health check

## 🐛 Bugs Found and Fixed During Development

### 1. **Missing LLM Configuration**
- **Bug**: `llm = llm` was undefined in `agents.py`
- **Fix**: Added proper LLM initialization with environment variable support
- **Impact**: System would crash on startup due to undefined variable

### 2. **Missing PDFLoader Import**
- **Bug**: `PDFLoader` was used in `tools.py` but not imported
- **Fix**: Added `from langchain_community.document_loaders import PyPDFLoader`
- **Impact**: PDF reading functionality would fail

### 3. **Incorrect Tool Implementation**
- **Bug**: Tools were defined as async functions but used synchronously
- **Fix**: Converted tools to proper CrewAI BaseTool classes with `_run` method
- **Impact**: Tool execution would fail due to async/sync mismatch

### 4. **Missing Dependencies**
- **Bug**: Several required packages missing from `requirements.txt`
- **Fix**: Added missing dependencies:
  - `python-dotenv==1.0.0`
  - `uvicorn==0.27.1`
  - `python-multipart==0.0.6`
  - `langchain==0.1.0`
  - `langchain-community==0.0.10`
  - `pypdf==3.17.4`
  - `google-generativeai==0.8.5`
- **Impact**: Installation would fail and runtime errors would occur

### 5. **Unprofessional Agent Descriptions**
- **Bug**: Agents had unprofessional, potentially harmful descriptions
- **Fix**: Rewritten all agents with professional, evidence-based medical personas
- **Impact**: System would provide inaccurate or dangerous medical advice

### 6. **Incorrect File Path Handling**
- **Bug**: Main.py used hardcoded file path instead of uploaded file
- **Fix**: Updated to use the actual uploaded file path
- **Impact**: System would analyze wrong file or fail to process uploaded files

### 7. **Hardcoded API Keys**
- **Bug**: API keys were hardcoded in the source code
- **Fix**: Moved to environment variables with proper validation
- **Impact**: Security vulnerability and potential key exposure

### 8. **Incorrect Gemini Model Name**
- **Bug**: Used `gemini-pro` which doesn't exist in current API
- **Fix**: Updated to `gemini-1.5-flash` and `gemini-1.5-pro`
- **Impact**: API calls would fail with 404 errors

### 9. **Missing Environment Configuration**
- **Bug**: No `.env.example` or `.gitignore` for environment variables
- **Fix**: Created proper environment setup files
- **Impact**: Users couldn't set up the project properly

### 10. **Limited Error Handling**
- **Bug**: Poor error handling for API failures and file processing
- **Fix**: Added comprehensive try-catch blocks and user-friendly error messages
- **Impact**: System would crash on common errors

## 🚀 Features

- **AI-Powered Analysis**: Uses Google Gemini AI for intelligent blood test interpretation
- **PDF Processing**: Extracts and analyzes text from blood test PDF reports
- **Comprehensive Insights**: Provides detailed analysis of various blood markers
- **Health Recommendations**: Offers personalized health and lifestyle suggestions
- **RESTful API**: Easy-to-use FastAPI endpoints for integration
- **Secure**: Environment-based API key management
- **Queue Worker Model**: Handles concurrent requests with Redis and Celery
- **Database Integration**: Persistent storage with SQLAlchemy
- **Real-time Status Tracking**: Monitor analysis progress
- **Scalable Architecture**: Production-ready with multiple workers

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **AI/LLM**: Google Gemini AI
- **PDF Processing**: PyPDF2
- **Document Processing**: LangChain
- **Agent Framework**: CrewAI (for advanced multi-agent analysis)
- **Queue System**: Redis + Celery
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Task Processing**: Background workers with concurrency

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Redis server (for queue management)
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Ajishi2/Bloodtest.git
cd Bloodtest
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your configuration:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./blood_test_analyzer.db
# For PostgreSQL: postgresql://user:password@localhost/blood_test_analyzer

# Queue Configuration (Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**Get your Gemini API key from:** [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. Start Redis Server

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Windows:** Download and install Redis from [redis.io](https://redis.io/download)

### 6. Start All Services

**Option A: Use the startup script (Recommended)**
```bash
python start_services.py
```

**Option B: Start manually**
```bash
# Terminal 1: Start Celery worker
celery -A celery_app worker --loglevel=info --concurrency=2

# Terminal 2: Start FastAPI server
python main.py
```

The API will be available at: `http://localhost:8000`

### 7. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Submit analysis request
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample.pdf" \
  -F "query=What are the key findings in my blood test?"

# Check analysis status (use the analysis_id from the response above)
curl http://localhost:8000/status/{analysis_id}

# List all analyses
curl http://localhost:8000/analyses
```

## 📖 API Documentation

### Endpoints

#### GET `/`
Health check endpoint
```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

#### GET `/health`
Comprehensive health check including database and queue status
```json
{
  "api": "healthy",
  "database": "healthy",
  "queue": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### POST `/analyze`
Queue a blood test analysis request (non-blocking)

**Parameters:**
- `file` (required): PDF file containing blood test results
- `query` (optional): Specific question about the blood test (default: "Summarise my Blood Test Report")

**Response:**
```json
{
  "status": "accepted",
  "analysis_id": "uuid-here",
  "task_id": "celery-task-id",
  "message": "Analysis request accepted. Use /status/{analysis_id} to check progress.",
  "file_processed": "blood_test_report.pdf"
}
```

#### GET `/status/{analysis_id}`
Get the status and results of an analysis

**Response:**
```json
{
  "analysis_id": "uuid-here",
  "status": "completed",
  "file_name": "blood_test_report.pdf",
  "query": "What are the key findings?",
  "created_at": "2024-01-15T10:30:00.000Z",
  "processing_time": 15.5,
  "file_size": 1024000,
  "analysis": "Detailed AI-generated analysis..."
}
```

#### GET `/analyses`
List all analyses with optional filtering

**Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 10)
- `status` (optional): Filter by status (pending, processing, completed, failed)

**Response:**
```json
{
  "analyses": [
    {
      "id": "uuid-here",
      "file_name": "blood_test_report.pdf",
      "status": "completed",
      "created_at": "2024-01-15T10:30:00.000Z",
      "processing_time": 15.5
    }
  ],
  "total": 25,
  "skip": 0,
  "limit": 10
}
```

#### DELETE `/analyses/{analysis_id}`
Delete an analysis record

**Response:**
```json
{
  "message": "Analysis deleted successfully"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `CELERY_BROKER_URL` | Redis broker URL | No (defaults to localhost) |
| `CELERY_RESULT_BACKEND` | Redis result backend URL | No (defaults to localhost) |

### Model Configuration

The application uses `gemini-1.5-flash` by default for faster responses. You can modify the model in `celery_app.py`:

```python
gemini_model = genai.GenerativeModel('gemini-1.5-flash')  # Fast
# or
gemini_model = genai.GenerativeModel('gemini-1.5-pro')    # More detailed
```

### Queue Configuration

- **Concurrency**: 2 workers by default (configurable)
- **Task Timeout**: 30 minutes maximum
- **Soft Timeout**: 25 minutes (graceful shutdown)
- **Auto-cleanup**: Old records removed after 30 days

## 📁 Project Structure

```
blood-test-analyser/
├── main.py              # FastAPI application entry point
├── models.py            # Database models (SQLAlchemy)
├── database.py          # Database configuration and session management
├── celery_app.py        # Celery configuration and background tasks
├── start_services.py    # Startup script for all services
├── agents.py            # CrewAI agent definitions
├── task.py              # Task definitions for agents
├── tools.py             # Custom tools for PDF processing
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── data/               # Sample data and uploads
│   └── sample.pdf      # Sample blood test report
└── outputs/            # Generated outputs
```

## 🔒 Security

- API keys are stored in environment variables
- `.env` files are excluded from version control
- Temporary files are automatically cleaned up
- Input validation and error handling implemented
- Database connections are properly managed
- Background tasks have timeout limits

## 🚀 Production Deployment

### Docker Setup (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=postgresql://user:password@db/blood_test_analyzer
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis
      - db
  
  worker:
    build: .
    command: celery -A celery_app worker --loglevel=info
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=postgresql://user:password@db/blood_test_analyzer
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=blood_test_analyzer
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important Medical Disclaimer:**

This application is for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

- The AI analysis provided is not a substitute for professional medical evaluation
- Results should be interpreted by qualified healthcare providers
- Do not make medical decisions based solely on this application's output
- The application may not detect all medical conditions or provide complete analysis

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/Ajishi2/Bloodtest/issues) page
2. Create a new issue with detailed information
3. Ensure your API key is valid and has sufficient quota
4. Verify Redis is running for queue functionality
5. Check database connectivity

## 🔄 Updates

- **v1.0.0**: Initial release with Gemini AI integration
- **v1.1.0**: Added CrewAI multi-agent framework support
- **v1.2.0**: Enhanced PDF processing and error handling
- **v1.3.0**: Fixed all major bugs and improved security
- **v2.0.0**: Added Queue Worker Model and Database Integration

---

**Made with ❤️ using FastAPI, Google Gemini AI, Redis, and Celery**
