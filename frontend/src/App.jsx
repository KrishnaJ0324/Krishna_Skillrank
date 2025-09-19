// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import JobListings from './components/JobListings';
import ResumeUpload from './components/ResumeUpload';
import ResultsPage from './components/ResultsPage';
import './App.css'; // Make sure this line is here

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<JobListings />} />
          <Route path="/upload" element={<ResumeUpload />} />
          <Route path="/results/:candidateId" element={<ResultsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;