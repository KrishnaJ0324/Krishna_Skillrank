import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables from your .env file
load_dotenv()

# Configure the Gemini API client with your key
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

def get_gemini_response(prompt):
    """A helper function to call the Gemini API and handle potential errors."""
    if not model:
        raise ConnectionError("Gemini API is not configured. Check your API key.")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None # Return None to indicate failure

def extract_skills(text_content, source_type="resume"):
    """
    Extracts skills from a given text (resume or job description).
    Returns a list of skills as strings.
    """
    prompt = f"""
    From the following {source_type} text, please extract all key technical skills and soft skills.
    Return the skills as a single, comma-separated string. Do not include any other text or explanation.

    Example: "React,JavaScript,Python,SQL,Teamwork,Communication,Agile Methodologies"

    Text to analyze:
    ---
    {text_content}
    ---
    """
    response_text = get_gemini_response(prompt)
    if response_text:
        # Clean up the response and split it into a list
        return [skill.strip() for skill in response_text.split(',') if skill.strip()]
    return []

# In backend/llm.py

def analyze_match(resume_skills, job_skills):
    """
    Compares resume skills and job skills to provide a detailed match analysis.
    Returns a dictionary with the analysis.
    """
    resume_skills_str = ", ".join(resume_skills)
    job_skills_str = ", ".join(job_skills)

    prompt = f"""
    Please perform a detailed analysis of the match between the skills from a resume and a job description.

    Resume Skills: "{resume_skills_str}"
    Job Skills: "{job_skills_str}"

    Provide your response in a strict JSON format ONLY. Do not include any markdown formatting like ```json.
    The JSON object must have the following keys:
    - "matching_skills": A list of skills present in both the resume and the job description.
    - "missing_skills": A list of skills required by the job but missing from the resume.
    - "match_score": An integer percentage (from 0 to 100) representing how well the resume skills match the job requirements. Calculate this score logically based on the overlap.
    - "explanation": A brief, one-sentence explanation for the score, highlighting a key strength or weakness.

    Example of the required JSON output format:
    {{
        "matching_skills": ["React", "JavaScript"],
        "missing_skills": ["Redux", "TypeScript"],
        "match_score": 82,
        "explanation": "The candidate shows strong fundamental web skills but lacks experience in advanced state management and static typing."
    }}
    """
    response_text = get_gemini_response(prompt)

    if response_text:
        try:
            # THE FIX IS HERE: Clean the string before parsing
            # This removes the ```json at the start and the ``` at the end
            clean_json_string = response_text.strip().replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json_string)
        except json.JSONDecodeError:
            print("Failed to decode JSON from Gemini response after cleaning. Raw response:")
            print(response_text)
            return None
    return None