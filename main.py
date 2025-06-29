from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import uuid
import asyncio
from typing import List, Optional
from datetime import datetime

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification

# Database and Queue imports
from database import get_db, init_db
from models import Analysis
from celery_app import process_blood_test_analysis, celery_app

# Gemini integration
import google.generativeai as genai
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required. Please set it in your .env file or environment.")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_with_gemini(prompt: str) -> str:
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {str(e)}"

app = FastAPI(title="Blood Test Report Analyser")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

def run_crew(query: str, file_path: str):
    """To run the whole crew (not used with Gemini)"""
    medical_crew = Crew(
        agents=[verifier, doctor, nutritionist, exercise_specialist],
        tasks=[verification, help_patients, nutrition_analysis, exercise_planning],
        process=Process.sequential,
    )
    result = medical_crew.kickoff({'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Analyze blood test report using queue worker model for concurrent processing"""
    analysis_id = str(uuid.uuid4())
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Create directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        content = await file.read()
        file_size = len(content)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        if not query:
            query = "Summarise my Blood Test Report"
        
        # Create analysis record in database
        analysis_record = Analysis(
            id=analysis_id,
            file_name=file.filename,
            original_query=query,
            analysis_result="",  # Will be updated by background task
            status="pending",
            file_size=file_size
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)
        
        # Start background task for processing
        task = process_blood_test_analysis.delay(analysis_id, file_path, query, file_size)
        
        return {
            "status": "accepted",
            "analysis_id": analysis_id,
            "task_id": task.id,
            "message": "Analysis request accepted. Use /status/{analysis_id} to check progress.",
            "file_processed": file.filename
        }
        
    except Exception as e:
        # Clean up file if it exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        
        # Update database with error
        try:
            analysis_record = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis_record:
                analysis_record.status = "failed"
                analysis_record.error_message = str(e)
                db.commit()
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")

@app.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: str, db: Session = Depends(get_db)):
    """Get the status and results of an analysis"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    response = {
        "analysis_id": analysis.id,
        "status": analysis.status,
        "file_name": analysis.file_name,
        "query": analysis.original_query,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
        "processing_time": analysis.processing_time,
        "file_size": analysis.file_size
    }
    
    if analysis.status == "completed":
        response["analysis"] = analysis.analysis_result
    elif analysis.status == "failed":
        response["error"] = analysis.error_message
    elif analysis.status == "processing":
        response["message"] = "Analysis is currently being processed"
    
    return response

@app.get("/analyses")
async def list_analyses(
    skip: int = 0, 
    limit: int = 10, 
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all analyses with optional filtering"""
    query = db.query(Analysis)
    
    if status:
        query = query.filter(Analysis.status == status)
    
    analyses = query.offset(skip).limit(limit).all()
    
    return {
        "analyses": [
            {
                "id": analysis.id,
                "file_name": analysis.file_name,
                "status": analysis.status,
                "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
                "processing_time": analysis.processing_time
            }
            for analysis in analyses
        ],
        "total": query.count(),
        "skip": skip,
        "limit": limit
    }

@app.delete("/analyses/{analysis_id}")
async def delete_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Delete an analysis record"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    db.delete(analysis)
    db.commit()
    
    return {"message": "Analysis deleted successfully"}

@app.get("/health")
async def health_check():
    """Comprehensive health check including database and queue"""
    health_status = {
        "api": "healthy",
        "database": "unknown",
        "queue": "unknown",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Check database
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        health_status["database"] = "healthy"
        db.close()
    except Exception as e:
        health_status["database"] = f"unhealthy: {str(e)}"
    
    # Check queue
    try:
        celery_app.control.inspect().active()
        health_status["queue"] = "healthy"
    except Exception as e:
        health_status["queue"] = f"unhealthy: {str(e)}"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)