# backend/schemas.py
from pydantic import BaseModel
from typing import List

class JobBase(BaseModel):
    title: str
    description: str
    company: str
    location: str

class Job(JobBase):
    id: int
    class Config:
        from_attributes = True

class Candidate(BaseModel):
    id: int
    name: str
    resume_text: str
    class Config:
        from_attributes = True

# backend/schemas.py
class MatchResponse(BaseModel):
    job_id: int
    title: str
    company: str      # Add this
    location: str     # Add this
    description: str  # Add this
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str