// src/components/ResumeUpload.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [extractedText, setExtractedText] = useState('');
  const [candidateId, setCandidateId] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }
    setUploading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload_resume', formData);
      setExtractedText(response.data.resume_text);
      setCandidateId(response.data.id);
    } catch (err) {
      setError('Failed to upload or process resume. Please try another file.');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const handleGetRecommendations = () => {
      if(candidateId) {
          navigate(`/results/${candidateId}`);
      }
  };

  return (
    <div className="container">
      <h1>Upload Your Resume</h1>
      <div className="card">
        <input type="file" onChange={handleFileChange} style={{ marginBottom: '1rem' }} />
        <button onClick={handleUpload} disabled={uploading || !file} className="btn btn-primary" style={{ width: '100%' }}>
          {uploading ? 'Processing...' : 'Upload and Process'}
        </button>
        {error && <p style={{ color: '#dc3545', marginTop: '1rem' }}>{error}</p>}
      </div>

      {extractedText && (
        <div className="card">
          <h2>Extracted Text</h2>
          <textarea readOnly value={extractedText}></textarea>
          <button onClick={handleGetRecommendations} className="btn btn-secondary" style={{ width: '100%', marginTop: '1rem' }}>
            Get Job Recommendations
          </button>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;