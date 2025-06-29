from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification

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
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations using Gemini"""
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        if not query:
            query = "Summarise my Blood Test Report"
        # Read the PDF content
        from tools import BloodTestReportTool
        pdf_tool = BloodTestReportTool()
        report_text = pdf_tool._run(file_path)
        # Compose the prompt for Gemini
        prompt = f"{query}\n\nHere is the blood test report:\n{report_text}"
        # Use Gemini for analysis
        analysis = analyze_with_gemini(prompt)
        return {
            "status": "success",
            "query": query,
            "analysis": analysis,
            "file_processed": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)