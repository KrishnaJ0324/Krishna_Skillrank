# backend/models.py
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    company = Column(String)
    location = Column(String)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Resume Candidate")
    resume_text = Column(Text)

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    score = Column(Float)
    matched_skills = Column(Text) # Storing as comma-separated string
    missing_skills = Column(Text) # Storing as comma-separated string