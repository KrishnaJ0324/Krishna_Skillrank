# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import pdfplumber
import io
import models
import schemas
import database
import llm


# Create all database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS Middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Allows your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Seed Data (for demonstration) ---
def seed_jobs(db: Session):
    if db.query(models.Job).count() == 0:
        jobs_data = [
            {"title": "Frontend Developer", "description": "We need a React and JavaScript expert. Experience with Redux and TypeScript is a plus.", "company": "Tech Solutions Inc.", "location": "New York, NY"},
            {"title": "Backend Python Developer", "description": "Seeking a developer skilled in Python, FastAPI, and SQL. Knowledge of Docker is essential.", "company": "Data Systems LLC", "location": "San Francisco, CA"},
            {"title": "Full-Stack Engineer", "description": "Join our team to work with React, Node.js, and PostgreSQL. We value teamwork and strong communication skills.", "company": "Innovatech", "location": "Remote"},
        ]
        for job_data in jobs_data:
            db.add(models.Job(**job_data))
        db.commit()

# Seed data on startup
@app.on_event("startup")
def on_startup():
    db = database.SessionLocal()
    seed_jobs(db)
    db.close()

# --- API Endpoints ---

@app.get("/jobs", response_model=List[schemas.Job])
def read_jobs(
    search: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of jobs with optional search and location filters.
    """
    query = db.query(models.Job)
    if search:
        query = query.filter(models.Job.title.contains(search))
    if location:
        query = query.filter(models.Job.location.contains(location))
    return query.all()

# The new, more powerful version using pdfplumber
 # Make sure to add this import at the top of your file!

@app.post("/upload_resume", response_model=schemas.Candidate)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a PDF resume, extract text using pdfplumber, and store it.
    """
    try:
        # Use a temporary file to work with pdfplumber
        with io.BytesIO(file.file.read()) as pdf_stream:
            text = ""
            with pdfplumber.open(pdf_stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        # Check if any text was extracted
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the PDF. The file might be an image.")

        new_candidate = models.Candidate(resume_text=text)
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)
        return new_candidate
    except Exception as e:
        # Be specific about the error if possible
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred during file processing: {str(e)}")
# We will add the /match_jobs endpoint in Phase 4
# In backend/main.py

@app.post("/match_jobs/{candidate_id}", response_model=List[schemas.MatchResponse]) # <-- Check this line carefully!
def match_jobs_for_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    jobs = db.query(models.Job).all()
    
    # 1. Extract skills from the resume ONCE.
    resume_skills = llm.extract_skills(candidate.resume_text, "resume")
    if not resume_skills:
        raise HTTPException(status_code=500, detail="Could not extract skills from resume.")

    all_matches = []

    for job in jobs:
        # 2. Extract skills for each job description.
        job_skills = llm.extract_skills(job.description, "job description")
        if not job_skills:
            continue # Skip job if skills can't be extracted
        
        # 3. Get analysis from Gemini.
        analysis = llm.analyze_match(resume_skills, job_skills)
        if not analysis:
            continue # Skip if analysis fails

        # Combine results into the response model
        match_response = schemas.MatchResponse(
    job_id=job.id,
    title=job.title,
    company=job.company,          # Add this
    location=job.location,      # Add this
    description=job.description,  # Add this
    match_score=analysis.get('match_score', 0),
    matching_skills=analysis.get('matching_skills', []),
    missing_skills=analysis.get('missing_skills', []),
    explanation=analysis.get('explanation', 'No explanation provided.')
)
        all_matches.append(match_response)

    # Sort matches by score in descending order
    sorted_matches = sorted(all_matches, key=lambda x: x.match_score, reverse=True)
    
    return sorted_matches