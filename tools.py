## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import BaseTool
from typing import Type

## Creating custom pdf reader tool
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Tool to read and extract data from blood test report PDF files"
    
    def _run(self, file_path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            file_path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        try:
            docs = PyPDFLoader(file_path=file_path).load()

            full_report = ""
            for data in docs:
                # Clean and format the report data
                content = data.page_content
                
                # Remove extra whitespaces and format properly
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                    
                full_report += content + "\n"
                
            return full_report
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

## Creating Nutrition Analysis Tool
class NutritionTool(BaseTool):
    name: str = "Nutrition Analysis Tool"
    description: str = "Analyzes blood test data and provides nutrition recommendations"
    
    def _run(self, blood_report_data: str) -> str:
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
class ExerciseTool(BaseTool):
    name: str = "Exercise Planning Tool"
    description: str = "Creates exercise plans based on blood test data"
    
    def _run(self, blood_report_data: str) -> str:        
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"