## Importing libraries and files
from crewai import Task

from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import BloodTestReportTool

## Creating a task to help solve user's query
help_patients = Task(
    description="""Analyze the blood test report and provide a comprehensive, professional analysis based on the user's query: {query}
    
    Your analysis should include:
    1. Summary of key findings from the blood test
    2. Identification of any abnormal values and their potential clinical significance
    3. Evidence-based recommendations based on the results
    4. Clear explanation of medical terms in understandable language
    5. Appropriate disclaimers about consulting healthcare providers for personalized advice
    
    Always prioritize accuracy, safety, and evidence-based practice.""",

    expected_output="""Provide a structured, professional blood test analysis including:
    - Executive summary of findings
    - Detailed analysis of abnormal values with reference ranges
    - Evidence-based recommendations
    - Clear medical explanations
    - Important disclaimers about consulting healthcare providers
    - Any red flags that require immediate medical attention""",

    agent=doctor,
    tools=[BloodTestReportTool()],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description="""Analyze the blood test results and provide evidence-based nutrition recommendations for the query: {query}
    
    Focus on:
    1. Nutritional implications of blood test results
    2. Dietary recommendations based on specific markers
    3. Evidence-based supplement recommendations (if applicable)
    4. Foods to include or avoid based on results
    5. Consultation with registered dietitians for personalized plans""",

    expected_output="""Provide comprehensive nutrition analysis including:
    - Nutritional interpretation of blood test markers
    - Specific dietary recommendations with scientific backing
    - Evidence-based supplement suggestions (if warranted)
    - Foods to include/avoid with explanations
    - Importance of professional nutrition consultation""",

    agent=nutritionist,
    tools=[BloodTestReportTool()],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description="""Create a safe, personalized exercise plan based on the blood test results for the query: {query}
    
    Consider:
    1. Exercise contraindications based on blood markers
    2. Safe exercise intensity and frequency recommendations
    3. Progressive training approaches
    4. Monitoring recommendations during exercise
    5. When to consult healthcare providers before starting exercise""",

    expected_output="""Provide a safe exercise plan including:
    - Exercise recommendations based on blood test results
    - Intensity and frequency guidelines
    - Safety considerations and contraindications
    - Progressive training approach
    - Monitoring and warning signs to watch for
    - Importance of medical clearance when appropriate""",

    agent=exercise_specialist,
    tools=[BloodTestReportTool()],
    async_execution=False,
)

## Creating a verification task
verification = Task(
    description="""Verify that the uploaded document is a legitimate blood test report and contains valid medical data.
    
    Check for:
    1. Presence of standard blood test markers
    2. Laboratory information and credentials
    3. Date and patient information
    4. Reference ranges and units
    5. Overall document structure and format""",

    expected_output="""Provide verification results including:
    - Confirmation of document type (blood test report)
    - Assessment of data quality and completeness
    - Identification of any missing critical information
    - Recommendations for additional testing if needed
    - Overall confidence in the report's validity""",

    agent=verifier,
    tools=[BloodTestReportTool()],
    async_execution=False
)