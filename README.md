# Blood Test Analyzer

A FastAPI-based application that uses Google Gemini AI to analyze blood test reports and provide comprehensive health insights. This project combines AI-powered analysis with medical knowledge to help users understand their blood test results.

## 🚀 Features

- **AI-Powered Analysis**: Uses Google Gemini AI for intelligent blood test interpretation
- **PDF Processing**: Extracts and analyzes text from blood test PDF reports
- **Comprehensive Insights**: Provides detailed analysis of various blood markers
- **Health Recommendations**: Offers personalized health and lifestyle suggestions
- **RESTful API**: Easy-to-use FastAPI endpoints for integration
- **Secure**: Environment-based API key management

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **AI/LLM**: Google Gemini AI
- **PDF Processing**: PyPDF2
- **Document Processing**: LangChain
- **Agent Framework**: CrewAI (for advanced multi-agent analysis)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
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

Edit the `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Get your Gemini API key from:** [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. Run the Application

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

### 6. Test the API

```bash
# Health check
curl http://localhost:8000/

# Analyze a blood test report
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample.pdf" \
  -F "query=What are the key findings in my blood test?"
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

#### POST `/analyze`
Analyze a blood test report

**Parameters:**
- `file` (required): PDF file containing blood test results
- `query` (optional): Specific question about the blood test (default: "Summarise my Blood Test Report")

**Response:**
```json
{
  "status": "success",
  "query": "What are the key findings in my blood test?",
  "analysis": "Detailed AI-generated analysis...",
  "file_processed": "blood_test_report.pdf"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |

### Model Configuration

The application uses `gemini-1.5-flash` by default for faster responses. You can modify the model in `main.py`:

```python
gemini_model = genai.GenerativeModel('gemini-1.5-flash')  # Fast
# or
gemini_model = genai.GenerativeModel('gemini-1.5-pro')    # More detailed
```

## 📁 Project Structure

```
blood-test-analyser/
├── main.py              # FastAPI application entry point
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

## 🔄 Updates

- **v1.0.0**: Initial release with Gemini AI integration
- **v1.1.0**: Added CrewAI multi-agent framework support
- **v1.2.0**: Enhanced PDF processing and error handling

---

**Made with ❤️ using FastAPI and Google Gemini AI**
