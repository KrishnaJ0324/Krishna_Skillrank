// src/components/ResultsPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const ResultsPage = () => {
  const { candidateId } = useParams();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRecommendations = async () => {
      if (!candidateId) return;
      setLoading(true);
      setError('');
      try {
        const response = await axios.post(`http://127.0.0.1:8000/match_jobs/${candidateId}`);
        setRecommendations(response.data);
      } catch (err) {
        setError('Failed to fetch recommendations. The AI analysis might have encountered an issue.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecommendations();
  }, [candidateId]);

  if (loading) {
    return (
      <div className="loader-container">
        <div className="loader"></div>
        <p>🧠 Analyzing your resume against job openings...</p>
      </div>
    );
  }

  if (error) {
    return <div style={{ textAlign: 'center', padding: '2rem', color: '#dc3545' }}>{error}</div>;
  }

  // In src/components/ResultsPage.jsx

  return (
    <div className="container">
      <header className="header">
        <h1>Your Personalized Job Matches</h1>
        <p>Based on our AI analysis of your resume</p>
      </header>
      
      {/* 1. Add the new result-grid wrapper div here */}
      <div className="result-grid"> 
        {recommendations.map((rec) => (
          <div key={rec.job_id} className="result-card">
            <div className="result-header">
              <div className="result-header-info">
                <h2>{rec.title}</h2>
                <p>{rec.company}, {rec.location}</p>
              </div>
              <div
                className="match-score-visual"
                style={{ '--score': rec.match_score }}
              >
                <span>{rec.match_score}%</span>
              </div>
            </div>

            <p className="ai-explanation">
              <strong>AI Insight:</strong> "{rec.explanation}"
            </p>

            <div className="skills-container">
              <div className="skills-list">
                <h3>✅ Matching Skills</h3>
                <div className="skill-pills">
                  {rec.matching_skills.map((skill, i) => (
                    <span key={i} className="skill-pill matching">{skill}</span>
                  ))}
                </div>
              </div>
              <div className="skills-list">
                <h3>❌ Missing Skills</h3>
                <div className="skill-pills">
                  {rec.missing_skills.map((skill, i) => (
                    <span key={i} className="skill-pill missing">{skill}</span>
                  ))}
                </div>
              </div>
            </div>

            <details className="job-details">
              <summary>View Full Job Description</summary>
              <p>{rec.description}</p>
            </details>
          </div>
        ))}
      </div> {/* 2. End of the new wrapper div */}
      
      <div style={{ textAlign: 'center', marginTop: '2rem', width: '100%' }}>
          <Link to="/upload" className="btn btn-primary">
              Upload Another Resume
          </Link>
      </div>
    </div>
  );
};

export default ResultsPage;