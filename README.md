
# 🩸 Blood Test Report Analyzer

A production-ready AI-powered blood test analysis system built with FastAPI, CrewAI, and Google Gemini. This application provides comprehensive medical analysis of blood test reports using advanced AI agents.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Multi-Agent System**: Uses CrewAI with specialized medical agents (Doctor, Nutritionist, Exercise Specialist, Verifier)
- **Google Gemini Integration**: Leverages Google's Gemini 1.5 Flash for intelligent medical analysis
- **Comprehensive Reports**: Detailed analysis covering CBC, liver function, lipids, diabetes markers, thyroid, and vitamins

### 🚀 Production-Ready Architecture
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Background Processing**: Celery + Redis for scalable task queue management
- **Database Storage**: SQLAlchemy with SQLite for persistent data storage
- **Health Monitoring**: Comprehensive health checks for all system components

### 📊 Analysis Capabilities
- **PDF Processing**: Extracts text from blood test PDF reports
- **Medical Interpretation**: AI-powered analysis of medical values and trends
- **Risk Assessment**: Identifies potential health risks and recommendations
- **Professional Reports**: Structured, medical-grade analysis output

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Celery        │    │   Redis         │
│   Server        │◄──►│   Worker        │◄──►│   Queue         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SQLite        │    │   Google        │    │   CrewAI        │
│   Database      │    │   Gemini        │    │   Agents        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Redis server
- Google Gemini API key

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd blood-test-analyser-debug
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./blood_test_analyzer.db
REDIS_URL=redis://localhost:6379/0
```

### 3. Start Services
```bash
# Terminal 1: Start Redis (if not running)
redis-server

# Terminal 2: Start Celery Worker
source venv/bin/activate
celery -A celery_app.celery_app worker --loglevel=info

# Terminal 3: Start FastAPI Server
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the System
```bash
# Health check
curl http://localhost:8000/health

# Upload a blood test report
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample.pdf" \
  -F "query=Analyze my blood test report"
```

## 📋 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health` - Comprehensive system health status
- `POST /analyze` - Upload and analyze blood test report
- `GET /status/{analysis_id}` - Check analysis progress
- `GET /analyses` - List all analyses
- `DELETE /analyses/{analysis_id}` - Delete analysis

### Example API Usage

#### Upload Blood Test Report
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@blood_test.pdf" \
  -F "query=Provide a comprehensive analysis of my blood test results"
```

**Response:**
```json
{
  "status": "accepted",
  "analysis_id": "1f153bf1-2b46-4de0-8726-0bb5f96cfe39",
  "task_id": "8f3db50d-abd7-4f4d-b659-22869f59daf1",
  "message": "Analysis request accepted. Use /status/{analysis_id} to check progress.",
  "file_processed": "blood_test.pdf"
}
```

#### Check Analysis Status
```bash
curl "http://localhost:8000/status/1f153bf1-2b46-4de0-8726-0bb5f96cfe39"
```

**Response:**
```json
{
  "analysis_id": "1f153bf1-2b46-4de0-8726-0bb5f96cfe39",
  "status": "completed",
  "file_name": "blood_test.pdf",
  "query": "Provide a comprehensive analysis of my blood test results",
  "created_at": "2025-06-29T10:13:21",
  "processing_time": 5.306822299957275,
  "file_size": 704703,
  "analysis": "This is a comprehensive blood test report for a 30-year-old male..."
}
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///./blood_test_analyzer.db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |

### Database Schema
```sql
CREATE TABLE analyses (
    id VARCHAR PRIMARY KEY,
    file_name VARCHAR,
    original_query TEXT,
    analysis_result TEXT,
    status VARCHAR,
    created_at DATETIME,
    processing_time FLOAT,
    file_size INTEGER,
    error_message TEXT
);
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "api": "healthy",
  "database": "healthy",
  "queue": "healthy",
  "timestamp": "2025-06-29T15:53:59.039"
}
```

### Sample Analysis
The system includes a sample PDF in `data/sample.pdf` for testing purposes.

## 📁 Project Structure
```
blood-test-analyser-debug/
├── main.py                 # FastAPI application
├── celery_app.py          # Celery configuration and tasks
├── database.py            # Database setup and utilities
├── models.py              # SQLAlchemy models
├── agents.py              # CrewAI agent definitions
├── task.py                # CrewAI task definitions
├── tools.py               # Custom tools for agents
├── requirements.txt       # Python dependencies
├── start_services.py      # Service startup script
├── data/                  # Sample data directory
│   └── sample.pdf         # Sample blood test report
├── outputs/               # Analysis output directory
└── venv/                  # Virtual environment
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Module Not Found Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Celery Worker Not Starting
```bash
# Check Redis is running
redis-cli ping

# Start Celery with proper module path
celery -A celery_app.celery_app worker --loglevel=info
```

#### 3. Database Connection Issues
```bash
# Check database file permissions
ls -la blood_test_analyzer.db

# Reinitialize database
python -c "from database import init_db; init_db()"
```

### Health Check Troubleshooting
- **API unhealthy**: Check FastAPI server logs
- **Database unhealthy**: Verify SQLite file permissions and path
- **Queue unhealthy**: Ensure Redis is running and accessible

## 🚀 Deployment

### Production Considerations
1. **Use PostgreSQL** instead of SQLite for production
2. **Configure Redis** with proper authentication
3. **Set up monitoring** for Celery workers
4. **Use environment variables** for all sensitive configuration
5. **Implement rate limiting** for API endpoints
6. **Add logging** for production debugging

### Docker Deployment
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `http://localhost:8000/docs`
3. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Web UI for easier interaction
- [ ] Support for more file formats (images, scanned documents)
- [ ] Historical analysis tracking
- [ ] Export reports to PDF/Word
- [ ] Integration with electronic health records
- [ ] Mobile app support

---
## 📸 Example Results

### Celery Worker Processing
![Celery Worker Processing]
<img width="893" alt="image" src="https://github.com/user-attachments/assets/75b4134e-6b84-4271-93cf-0fbf50fac396" />


### API Analysis Result
![API Analysis Result]
<img width="878" alt="image" src="https://github.com/user-attachments/assets/e0a98608-d422-472d-9505-03adffe4429b" />

**Built with ❤️ using FastAPI, CrewAI, and Google Gemini**
