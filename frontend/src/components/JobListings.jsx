// src/components/JobListings.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const JobListings = () => {
  const [jobs, setJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [locationFilter, setLocationFilter] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/jobs', {
          params: {
            search: searchTerm,
            location: locationFilter,
          },
        });
        setJobs(response.data);
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };

    const handler = setTimeout(() => {
      fetchJobs();
    }, 300);

    return () => {
      clearTimeout(handler);
    };
  }, [searchTerm, locationFilter]);

  return (
    <div className="container">
      {/* 1. Added a new, more attractive header */}
      <header className="header">
        <h1>Find Your Next Opportunity</h1>
        <p>Browse through thousands of job listings from top companies.</p>
      </header>

      {/* 2. Wrapped filters in a new div for better styling */}
      <div className="filter-controls">
        <input
          type="text"
          placeholder="Filter by job title, skill..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input-field"
        />
        <input
          type="text"
          placeholder="Filter by location..."
          value={locationFilter}
          onChange={(e) => setLocationFilter(e.target.value)}
          className="input-field"
        />
        <Link to="/upload" className="btn btn-primary">
          Upload Resume
        </Link>
      </div>

      {/* 3. Updated the job grid and card structure */}
      <div className="job-grid">
        {jobs.length > 0 ? (
          jobs.map((job) => (
            <div key={job.id} className="card">
              <h2>{job.title}</h2>
              <p className="card-company">{job.company}</p>
              <p className="card-location">{job.location}</p>
              <p className="card-description">{job.description}</p>
            </div>
          ))
        ) : (
          <p className="no-jobs">No jobs found matching your criteria.</p>
        )}
      </div>
    </div>
  );
};

export default JobListings;