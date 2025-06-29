from celery import Celery
import os
import time
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Analysis
import google.generativeai as genai
from tools import BloodTestReportTool

# Celery configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Initialize Celery
celery_app = Celery(
    "blood_test_analyzer",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["celery_app"]
)

# Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_with_gemini(prompt: str) -> str:
    """Analyze text using Gemini AI"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {str(e)}"

@celery_app.task(bind=True)
def process_blood_test_analysis(self, analysis_id: str, file_path: str, query: str, file_size: int = None):
    """Background task to process blood test analysis"""
    start_time = time.time()
    
    try:
        # Update status to processing
        db = SessionLocal()
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.status = "processing"
            db.commit()
        
        # Process the PDF
        pdf_tool = BloodTestReportTool()
        report_text = pdf_tool._run(file_path)
        
        # Compose the prompt for Gemini
        prompt = f"{query}\n\nHere is the blood test report:\n{report_text}"
        
        # Use Gemini for analysis
        analysis_result = analyze_with_gemini(prompt)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update database with results
        if analysis:
            analysis.analysis_result = analysis_result
            analysis.status = "completed"
            analysis.processing_time = processing_time
            analysis.file_size = file_size
            db.commit()
        
        # Clean up temporary file
        try:
            os.remove(file_path)
        except:
            pass
        
        return {
            "status": "success",
            "analysis_id": analysis_id,
            "processing_time": processing_time,
            "result": analysis_result
        }
        
    except Exception as e:
        # Update database with error
        db = SessionLocal()
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.status = "failed"
            analysis.error_message = str(e)
            db.commit()
        
        # Clean up temporary file
        try:
            os.remove(file_path)
        except:
            pass
        
        raise e
    
    finally:
        db.close()

@celery_app.task
def cleanup_old_analyses():
    """Clean up old analysis records (older than 30 days)"""
    from datetime import datetime, timedelta
    from sqlalchemy import and_
    
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        old_analyses = db.query(Analysis).filter(
            and_(
                Analysis.created_at < cutoff_date,
                Analysis.status.in_(["completed", "failed"])
            )
        ).all()
        
        for analysis in old_analyses:
            db.delete(analysis)
        
        db.commit()
        return f"Cleaned up {len(old_analyses)} old analysis records"
    
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close() 