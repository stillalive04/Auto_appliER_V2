import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface JobListing {
  id: string;
  title: string;
  company: string;
  company_url: string;
  location: string;
  job_url: string;
  salary_range: string;
  employment_type: string;
  job_type: string;
  remote: boolean;
  description: string;
  requirements: string[];
  posted_date: string;
  source: string;
  can_apply: boolean;
  match_score: number;
  experience_level?: string;
}

const JobSearch: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useState({
    job_title: '',
    location: '',
    remote_ok: true,
    experience_level: 'mid',
    employment_type: 'Full-time',
    salary_min: 0,
    salary_max: 200000
  });
  
  const [jobs, setJobs] = useState<JobListing[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [totalJobs, setTotalJobs] = useState(0);
  const [applying, setApplying] = useState<string | null>(null);
  const [jobTitles, setJobTitles] = useState<any>({});
  const [locations, setLocations] = useState<any[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  // Load job titles and locations on component mount
  useEffect(() => {
    const loadData = async () => {
      try {
        const [jobTitlesResponse, locationsResponse] = await Promise.all([
          fetch('http://localhost:8000/api/job-titles'),
          fetch('http://localhost:8000/api/locations')
        ]);

        const jobTitlesData = await jobTitlesResponse.json();
        const locationsData = await locationsResponse.json();

        setJobTitles(jobTitlesData);
        setLocations(locationsData.locations || []);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setLoadingData(false);
      }
    };

    loadData();
  }, []);

  const handleInputChange = (field: string, value: any) => {
    setSearchParams(prev => ({ ...prev, [field]: value }));
  };

  const searchJobs = async () => {
    if (!searchParams.job_title.trim()) {
      alert('Please enter a job title');
      return;
    }

    setLoading(true);
    setSearched(true);

    try {
      const searchRequest = {
        job_title: searchParams.job_title,
        location: searchParams.location,
        limit: 1000, // Search for up to 1000 jobs
        experience_level: searchParams.experience_level,
        remote_only: searchParams.remote_ok,
        salary_min: searchParams.salary_min,
        salary_max: searchParams.salary_max
      };

      const response = await fetch('http://localhost:8000/search-jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchRequest)
      });

      const data = await response.json();

      if (response.ok) {
        setJobs(data.jobs || []);
        setTotalJobs(data.total || 0);
        
        // Show success message with platform info
        if (data.message) {
          console.log(data.message);
        }
      } else {
        alert(`Error searching for jobs: ${data.detail || 'Please try again.'}`);
      }
    } catch (error) {
      console.error('Error searching jobs:', error);
      alert('Error searching for jobs. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const applyToJob = async (job: JobListing) => {
    setApplying(job.id);

    try {
      const response = await fetch('http://localhost:8000/apply-to-job', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: '1',
          job_id: job.id,
          job_title: job.title,
          company: job.company,
          job_url: job.job_url
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(`Successfully applied to ${job.title} at ${job.company}!`);
      } else {
        alert(`Application failed: ${data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error applying to job:', error);
      alert('Error applying to job. Please try again.');
    } finally {
      setApplying(null);
    }
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'bg-green-100 text-green-800';
    if (score >= 80) return 'bg-blue-100 text-blue-800';
    if (score >= 70) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getSourceIcon = (source: string) => {
    switch (source.toLowerCase()) {
      case 'linkedin':
        return '💼';
      case 'indeed':
        return '🔍';
      case 'glassdoor':
        return '🏢';
      case 'handshake':
        return '🤝';
      case 'county news':
        return '📰';
      default:
        return '🌐';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Find Your Dream Job</h1>
          <p className="text-gray-600 text-lg">
            Search across LinkedIn, Indeed, Glassdoor, Handshake, and County Newspapers
          </p>
          <p className="text-gray-500">
            Covering all United States and Canada
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Title *
              </label>
              {loadingData ? (
                <div className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50">
                  Loading job titles...
                </div>
              ) : (
                <select
                  value={searchParams.job_title}
                  onChange={(e) => handleInputChange('job_title', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select a job title...</option>
                  {jobTitles.categories && Object.entries(jobTitles.categories).map(([category, titles]: [string, any]) => (
                    <optgroup key={category} label={category}>
                      {titles.map((title: string) => (
                        <option key={title} value={title}>{title}</option>
                      ))}
                    </optgroup>
                  ))}
                  {jobTitles.trending && jobTitles.trending.length > 0 && (
                    <optgroup label="🔥 Trending">
                      {jobTitles.trending.map((title: string) => (
                        <option key={title} value={title}>{title}</option>
                      ))}
                    </optgroup>
                  )}
                </select>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              {loadingData ? (
                <div className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50">
                  Loading locations...
                </div>
              ) : (
                <select
                  value={searchParams.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All United States & Canada</option>
                  {locations.map((location: any) => (
                    <option key={location.value} value={location.value}>
                      {location.label}
                    </option>
                  ))}
                </select>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Experience Level
              </label>
              <select
                value={searchParams.experience_level}
                onChange={(e) => handleInputChange('experience_level', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="internship">Internship</option>
                <option value="entry">Entry Level</option>
                <option value="junior">Junior</option>
                <option value="mid">Mid Level</option>
                <option value="senior">Senior</option>
                <option value="lead">Lead</option>
                <option value="principal">Principal</option>
                <option value="manager">Manager</option>
                <option value="director">Director</option>
                <option value="vp">VP</option>
                <option value="c_suite">C-Suite</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Employment Type
              </label>
              <select
                value={searchParams.employment_type}
                onChange={(e) => handleInputChange('employment_type', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="W2">W2 Employee</option>
                <option value="C2H">Contract-to-Hire</option>
                <option value="1099">1099 Contractor</option>
                <option value="Freelance">Freelance</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Min Salary ($)
              </label>
              <input
                type="number"
                value={searchParams.salary_min}
                onChange={(e) => handleInputChange('salary_min', parseInt(e.target.value) || 0)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Salary ($)
              </label>
              <input
                type="number"
                value={searchParams.salary_max}
                onChange={(e) => handleInputChange('salary_max', parseInt(e.target.value) || 200000)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                min="0"
              />
            </div>
          </div>

          <div className="mt-6 flex items-center space-x-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={searchParams.remote_ok}
                onChange={(e) => handleInputChange('remote_ok', e.target.checked)}
                className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Include remote work</span>
            </label>
          </div>

          <div className="mt-6">
            <button
              onClick={searchJobs}
              disabled={loading}
              className="w-full md:w-auto px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Searching...
                </div>
              ) : (
                '🔍 Search Jobs'
              )}
            </button>
          </div>
        </div>

        {/* Search Results */}
        {searched && (
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {loading ? 'Searching...' : `Found ${totalJobs} jobs`}
            </h2>
            {!loading && totalJobs > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                  💼 LinkedIn
                </span>
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                  🔍 Indeed
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
                  🏢 Glassdoor
                </span>
                <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                  🤝 Handshake
                </span>
                <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                  📰 County News
                </span>
              </div>
            )}
          </div>
        )}

        {/* Job Listings */}
        <div className="space-y-6">
          {jobs.map((job) => (
            <div key={job.id} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-xl font-bold text-gray-900">{job.title}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getMatchScoreColor(job.match_score)}`}>
                      {job.match_score}% match
                    </span>
                    <span className="text-lg">{getSourceIcon(job.source)}</span>
                  </div>
                  <div className="flex items-center space-x-4 text-gray-600 mb-2">
                    <span className="font-medium">{job.company}</span>
                    <span>•</span>
                    <span>{job.location}</span>
                    <span>•</span>
                    <span>{job.posted_date}</span>
                    {job.remote && (
                      <>
                        <span>•</span>
                        <span className="text-green-600">Remote</span>
                      </>
                    )}
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-500 mb-4">
                    <span>{job.employment_type}</span>
                    <span>•</span>
                    <span>{job.salary_range}</span>
                    <span>•</span>
                    <span>{job.source}</span>
                  </div>
                </div>
                <div className="flex flex-col space-y-2">
                  <button
                    onClick={() => applyToJob(job)}
                    disabled={applying === job.id}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {applying === job.id ? 'Applying...' : 'Quick Apply'}
                  </button>
                  <a
                    href={job.job_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-center"
                  >
                    View Job
                  </a>
                </div>
              </div>

              <p className="text-gray-700 mb-4 line-clamp-3">
                {job.description}
              </p>

              {job.requirements && job.requirements.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Requirements:</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.requirements.slice(0, 8).map((req, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm"
                      >
                        {req}
                      </span>
                    ))}
                    {job.requirements.length > 8 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-500 rounded text-sm">
                        +{job.requirements.length - 8} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between text-sm text-gray-500">
                <span>Posted {job.posted_date}</span>
                <a
                  href={job.company_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                >
                  View Company →
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* No Results */}
        {searched && !loading && jobs.length === 0 && (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No jobs found</h3>
            <p className="text-gray-600">
              Try adjusting your search criteria or location
            </p>
          </div>
        )}

        {/* Back to Dashboard */}
        <div className="text-center mt-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobSearch; 