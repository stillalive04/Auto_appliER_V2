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
}

interface ProfileCompleteness {
  is_complete: boolean;
  completion_percentage: number;
  missing_fields: string[];
  message: string;
}

interface Application {
  id: string;
  job_title: string;
  company: string;
  status: string;
  applied_at: string;
  job_url: string;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [jobListings, setJobListings] = useState<JobListing[]>([]);
  const [profileCompleteness, setProfileCompleteness] = useState<ProfileCompleteness | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [applyingJobs, setApplyingJobs] = useState<Set<string>>(new Set());
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }

    const parsedUser = JSON.parse(userData);
    setUser(parsedUser);
    fetchDashboardData(parsedUser.id);
  }, [navigate]);

  const fetchDashboardData = async (userId: string) => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [jobsResponse, profileResponse, notificationsResponse] = await Promise.all([
        fetch(`http://localhost:8000/job-listings/${userId}`),
        fetch(`http://localhost:8000/profile-completeness/${userId}`),
        fetch(`http://localhost:8000/notifications/${userId}`)
      ]);

      if (jobsResponse.ok) {
        const jobsData = await jobsResponse.json();
        setJobListings(jobsData.jobs || []);
      }

      if (profileResponse.ok) {
        const profileData = await profileResponse.json();
        setProfileCompleteness(profileData);
      }

      if (notificationsResponse.ok) {
        const notificationsData = await notificationsResponse.json();
        setNotifications(notificationsData.notifications || []);
      }

      // Fetch applications from the applications database
      const applicationsResponse = await fetch(`http://localhost:8000/debug/database`);
      if (applicationsResponse.ok) {
        const dbData = await applicationsResponse.json();
        const userApplications = dbData.applications?.filter((app: any) => app.user_id === userId) || [];
        setApplications(userApplications);
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyToJob = async (job: JobListing) => {
    if (!user) return;

    setApplyingJobs(prev => new Set(prev).add(job.id));

    try {
      const response = await fetch('http://localhost:8000/apply-to-job', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_id: job.id,
          user_id: user.id,
          job_title: job.title,
          company: job.company,
          job_url: job.job_url
        }),
      });

      const result = await response.json();

      if (result.success) {
        alert(`✅ Successfully applied to ${job.title} at ${job.company}!`);
        // Refresh applications
        fetchDashboardData(user.id);
      } else {
        if (result.error === "Profile incomplete") {
          alert(`❌ Cannot apply: ${result.message}\n\nMissing: ${result.missing_fields.join(', ')}`);
        } else if (result.retry_possible) {
          const retry = confirm(`❌ Application failed: ${result.error}\n\nWould you like to apply manually?`);
          if (retry && result.manual_application_url) {
            window.open(result.manual_application_url, '_blank');
          }
        } else {
          alert(`❌ Application failed: ${result.error}`);
        }
      }
    } catch (error) {
      console.error('Error applying to job:', error);
      alert('❌ Error applying to job. Please try again.');
    } finally {
      setApplyingJobs(prev => {
        const newSet = new Set(prev);
        newSet.delete(job.id);
        return newSet;
      });
    }
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted': return 'text-green-600 bg-green-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'rejected': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AutoJobApply Dashboard</h1>
              <p className="text-gray-600">Welcome back, {user?.name}!</p>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => navigate('/profile')}
                className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
              >
                Edit Profile
              </button>
              <button
                onClick={() => {
                  localStorage.removeItem('user');
                  navigate('/');
                }}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Completeness Alert */}
        {profileCompleteness && !profileCompleteness.is_complete && (
          <div className="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <h3 className="text-sm font-medium text-yellow-800">Profile Incomplete</h3>
                <p className="text-sm text-yellow-700 mt-1">{profileCompleteness.message}</p>
                <div className="mt-2">
                  <div className="bg-yellow-200 rounded-full h-2">
                    <div 
                      className="bg-yellow-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${profileCompleteness.completion_percentage}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-yellow-600 mt-1">{profileCompleteness.completion_percentage}% complete</p>
                </div>
              </div>
              <button
                onClick={() => navigate('/profile')}
                className="ml-3 px-3 py-1 bg-yellow-600 text-white text-sm rounded hover:bg-yellow-700 transition-colors"
              >
                Complete Profile
              </button>
            </div>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Available Jobs</p>
                <p className="text-2xl font-bold text-gray-900">{jobListings.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Applications Sent</p>
                <p className="text-2xl font-bold text-gray-900">{applications.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM4 19h9v-2H4v2zM4 15h9v-2H4v2zM4 11h9V9H4v2z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Profile Complete</p>
                <p className="text-2xl font-bold text-gray-900">{profileCompleteness?.completion_percentage || 0}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM4 19h9v-2H4v2zM4 15h9v-2H4v2zM4 11h9V9H4v2z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Notifications</p>
                <p className="text-2xl font-bold text-gray-900">{notifications.length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Job Listings */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Available Job Opportunities</h2>
            <p className="text-sm text-gray-600">Real job openings from top companies</p>
          </div>
          <div className="divide-y divide-gray-200">
            {jobListings.length === 0 ? (
              <div className="p-6 text-center text-gray-500">
                <p>No job listings available. Please check your preferences.</p>
              </div>
            ) : (
              jobListings.map((job) => (
                <div key={job.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getMatchScoreColor(job.match_score)}`}>
                          {job.match_score}% match
                        </span>
                        {job.remote && (
                          <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                            Remote
                          </span>
                        )}
                      </div>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                        <span className="font-medium text-gray-900">{job.company}</span>
                        <span>•</span>
                        <span>{job.location}</span>
                        <span>•</span>
                        <span>{job.salary_range}</span>
                        <span>•</span>
                        <span className="font-medium">{job.employment_type}</span>
                      </div>

                      <p className="text-gray-700 mb-3 line-clamp-2">{job.description}</p>

                      <div className="flex flex-wrap gap-2 mb-3">
                        {job.requirements.slice(0, 4).map((req, index) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                            {req}
                          </span>
                        ))}
                        {job.requirements.length > 4 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                            +{job.requirements.length - 4} more
                          </span>
                        )}
                      </div>

                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>Posted: {new Date(job.posted_date).toLocaleDateString()}</span>
                        <span>•</span>
                        <span>Source: {job.source}</span>
                        <span>•</span>
                        <a 
                          href={job.job_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 underline"
                        >
                          View Original Posting
                        </a>
                      </div>
                    </div>

                    <div className="ml-6 flex flex-col space-y-2">
                      <button
                        onClick={() => applyToJob(job)}
                        disabled={applyingJobs.has(job.id) || !job.can_apply}
                        className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                          applyingJobs.has(job.id)
                            ? 'bg-gray-400 text-white cursor-not-allowed'
                            : job.can_apply
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        }`}
                      >
                        {applyingJobs.has(job.id) ? 'Applying...' : 'Quick Apply'}
                      </button>
                      
                      <a
                        href={job.company_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-center text-sm"
                      >
                        Company Page
                      </a>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Applications */}
        {applications.length > 0 && (
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Recent Applications</h2>
              <p className="text-sm text-gray-600">Track your job application status</p>
            </div>
            <div className="divide-y divide-gray-200">
              {applications.slice(0, 5).map((app) => (
                <div key={app.id} className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">{app.job_title}</h3>
                      <p className="text-sm text-gray-600">{app.company}</p>
                      <p className="text-xs text-gray-500">Applied: {new Date(app.applied_at).toLocaleDateString()}</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(app.status)}`}>
                        {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                      </span>
                      {app.job_url && (
                        <a
                          href={app.job_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 text-sm"
                        >
                          View Job
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 