import asyncio
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

@dataclass
class JobListing:
    title: str
    company: str
    location: str
    description: str
    salary: str
    employment_type: str
    posted_date: str
    apply_url: str
    source: str
    skills: List[str]
    experience_level: str
    remote_work: bool
    match_score: int

class RealisticJobGenerator:
    """
    Generates realistic job listings that actually match the search query
    with proper company-role-location matching and working search URLs.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define realistic job mappings based on actual job market
        self.job_mappings = {
            # Marketing roles
            "marketing analyst": {
                "companies": ["HubSpot", "Salesforce", "Adobe", "Google", "Meta", "Microsoft", "Amazon", "Netflix", "Spotify", "Airbnb"],
                "locations": ["New York, NY", "San Francisco, CA", "Los Angeles, CA", "Chicago, IL", "Boston, MA", "Seattle, WA", "Austin, TX", "Remote"],
                "salary_range": (45000, 95000),
                "skills": ["Google Analytics", "Excel", "SQL", "A/B Testing", "SEO", "SEM", "Data Analysis", "Marketing Automation", "CRM", "Tableau"],
                "remote_friendly": True
            },
            "marketing": {
                "companies": ["HubSpot", "Salesforce", "Adobe", "Google", "Meta", "Microsoft", "Amazon", "Netflix", "Spotify", "Airbnb"],
                "locations": ["New York, NY", "San Francisco, CA", "Los Angeles, CA", "Chicago, IL", "Boston, MA", "Seattle, WA", "Austin, TX", "Remote"],
                "salary_range": (45000, 95000),
                "skills": ["Google Analytics", "Excel", "SQL", "A/B Testing", "SEO", "SEM", "Data Analysis", "Marketing Automation", "CRM", "Tableau"],
                "remote_friendly": True
            },
            "digital marketing": {
                "companies": ["HubSpot", "Salesforce", "Adobe", "Google", "Meta", "Microsoft", "Amazon", "Netflix", "Spotify", "Airbnb"],
                "locations": ["New York, NY", "San Francisco, CA", "Los Angeles, CA", "Chicago, IL", "Boston, MA", "Seattle, WA", "Austin, TX", "Remote"],
                "salary_range": (45000, 95000),
                "skills": ["Google Analytics", "Facebook Ads", "Google Ads", "SEO", "SEM", "Content Marketing", "Email Marketing", "Social Media", "PPC"],
                "remote_friendly": True
            },
            
            # Software Engineering roles
            "software engineer": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (80000, 200000),
                "skills": ["Python", "Java", "JavaScript", "React", "Node.js", "AWS", "Docker", "Git", "SQL", "REST APIs"],
                "remote_friendly": True
            },
            "software developer": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (80000, 200000),
                "skills": ["Python", "Java", "JavaScript", "React", "Node.js", "AWS", "Docker", "Git", "SQL", "REST APIs"],
                "remote_friendly": True
            },
            "frontend developer": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (70000, 180000),
                "skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Vue.js", "Angular", "Webpack", "Git", "REST APIs"],
                "remote_friendly": True
            },
            "backend developer": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (85000, 190000),
                "skills": ["Python", "Java", "Node.js", "Go", "SQL", "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes"],
                "remote_friendly": True
            },
            
            # Data roles
            "data scientist": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify", "Tesla"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (90000, 180000),
                "skills": ["Python", "R", "SQL", "Machine Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Jupyter", "Statistics"],
                "remote_friendly": True
            },
            "data analyst": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify", "Tesla"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (60000, 120000),
                "skills": ["SQL", "Python", "R", "Excel", "Tableau", "Power BI", "Statistics", "Data Visualization", "ETL", "Analytics"],
                "remote_friendly": True
            },
            
            # Design roles
            "ux designer": {
                "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb", "Stripe", "Shopify"],
                "locations": ["San Francisco, CA", "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Remote"],
                "salary_range": (70000, 150000),
                "skills": ["Figma", "Sketch", "Adobe XD", "Prototyping", "User Research", "Wireframing", "Design Systems", "Usability Testing"],
                "remote_friendly": True
            },
            "graphic designer": {
                "companies": ["Adobe", "Nike", "Coca-Cola", "Apple", "Google", "Meta", "Netflix", "Spotify", "Airbnb", "Uber"],
                "locations": ["New York, NY", "Los Angeles, CA", "San Francisco, CA", "Chicago, IL", "Boston, MA", "Remote"],
                "salary_range": (45000, 85000),
                "skills": ["Adobe Creative Suite", "Photoshop", "Illustrator", "InDesign", "Figma", "Branding", "Typography", "Print Design"],
                "remote_friendly": True
            },
            
            # Sales roles
            "sales representative": {
                "companies": ["Salesforce", "Oracle", "Microsoft", "Amazon", "Google", "Adobe", "HubSpot", "Zoom", "Slack", "Dropbox"],
                "locations": ["New York, NY", "San Francisco, CA", "Chicago, IL", "Boston, MA", "Atlanta, GA", "Remote"],
                "salary_range": (45000, 120000),
                "skills": ["CRM", "Salesforce", "Cold Calling", "Lead Generation", "Negotiation", "Pipeline Management", "B2B Sales", "Account Management"],
                "remote_friendly": True
            },
            
            # Legal roles
            "attorney": {
                "companies": ["Skadden", "Baker McKenzie", "Latham & Watkins", "Kirkland & Ellis", "Sullivan & Cromwell", "Cravath", "Wachtell"],
                "locations": ["New York, NY", "Washington, DC", "Los Angeles, CA", "Chicago, IL", "Boston, MA", "San Francisco, CA"],
                "salary_range": (120000, 350000),
                "skills": ["Legal Research", "Contract Review", "Litigation", "Corporate Law", "Regulatory Compliance", "Legal Writing", "Client Relations"],
                "remote_friendly": False
            },
            "lawyer": {
                "companies": ["Skadden", "Baker McKenzie", "Latham & Watkins", "Kirkland & Ellis", "Sullivan & Cromwell", "Cravath", "Wachtell"],
                "locations": ["New York, NY", "Washington, DC", "Los Angeles, CA", "Chicago, IL", "Boston, MA", "San Francisco, CA"],
                "salary_range": (120000, 350000),
                "skills": ["Legal Research", "Contract Review", "Litigation", "Corporate Law", "Regulatory Compliance", "Legal Writing", "Client Relations"],
                "remote_friendly": False
            },
            
            # Healthcare roles
            "nurse": {
                "companies": ["Kaiser Permanente", "Mayo Clinic", "Cleveland Clinic", "Johns Hopkins", "Mount Sinai", "Cedars-Sinai", "NYU Langone"],
                "locations": ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Boston, MA", "Houston, TX", "Philadelphia, PA"],
                "salary_range": (60000, 95000),
                "skills": ["Patient Care", "Medical Records", "IV Therapy", "Medication Administration", "CPR", "BLS", "Electronic Health Records"],
                "remote_friendly": False
            },
            
            # Finance roles
            "financial analyst": {
                "companies": ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "Bank of America", "Wells Fargo", "Citigroup", "BlackRock"],
                "locations": ["New York, NY", "Chicago, IL", "Boston, MA", "San Francisco, CA", "Charlotte, NC", "Remote"],
                "salary_range": (70000, 130000),
                "skills": ["Financial Modeling", "Excel", "SQL", "Python", "R", "Bloomberg Terminal", "Valuation", "Risk Analysis", "Financial Reporting"],
                "remote_friendly": True
            },
            
            # Customer Service roles
            "customer service": {
                "companies": ["Amazon", "Apple", "Microsoft", "Google", "Salesforce", "Zoom", "Slack", "Dropbox", "Shopify", "Stripe"],
                "locations": ["Austin, TX", "Phoenix, AZ", "Tampa, FL", "Nashville, TN", "Remote"],
                "salary_range": (35000, 55000),
                "skills": ["Customer Support", "CRM", "Zendesk", "Communication", "Problem Solving", "Multi-tasking", "Phone Support", "Email Support"],
                "remote_friendly": True
            },
            
            # Administrative roles
            "administrative assistant": {
                "companies": ["Various Companies", "Law Firms", "Healthcare Systems", "Financial Services", "Government Agencies"],
                "locations": ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ", "Philadelphia, PA"],
                "salary_range": (35000, 55000),
                "skills": ["Microsoft Office", "Scheduling", "Data Entry", "Filing", "Phone Support", "Email Management", "Calendar Management"],
                "remote_friendly": True
            },
            
            # Receptionist roles - Limited realistic scenarios
            "receptionist": {
                "companies": ["Medical Offices", "Law Firms", "Corporate Offices", "Dental Practices", "Veterinary Clinics"],
                "locations": ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ", "Philadelphia, PA"],
                "salary_range": (30000, 45000),
                "skills": ["Phone Support", "Scheduling", "Customer Service", "Microsoft Office", "Multi-line Phone System", "Appointment Scheduling"],
                "remote_friendly": False
            }
        }
        
        # Experience level variations
        self.experience_levels = {
            "entry": {"prefix": "Entry-Level", "multiplier": 0.8},
            "junior": {"prefix": "Junior", "multiplier": 0.9},
            "mid": {"prefix": "", "multiplier": 1.0},
            "senior": {"prefix": "Senior", "multiplier": 1.3},
            "lead": {"prefix": "Lead", "multiplier": 1.5},
            "principal": {"prefix": "Principal", "multiplier": 1.7},
            "staff": {"prefix": "Staff", "multiplier": 1.6},
            "manager": {"prefix": "Manager", "multiplier": 1.4}
        }
        
        # Job sources with their URL patterns
        self.job_sources = {
            "Indeed": "https://www.indeed.com/jobs?q={query}&l={location}&fromage=7",
            "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&f_TPR=r604800",
            "Glassdoor": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locT=C&locId=&jobType=&fromAge=7",
            "Handshake": "https://www.handshake.com/jobs/search?query={query}&location={location}",
            "County Jobs": "https://countyjobs.com/search?q={query}&location={location}"
        }
    
    def _normalize_job_title(self, job_title: str) -> str:
        """Normalize job title to match our mappings"""
        normalized = job_title.lower().strip()
        
        # Handle common variations
        if "marketing" in normalized:
            if "analyst" in normalized:
                return "marketing analyst"
            elif "digital" in normalized:
                return "digital marketing"
            else:
                return "marketing"
        elif "software" in normalized and ("engineer" in normalized or "developer" in normalized):
            return "software engineer"
        elif "frontend" in normalized or "front-end" in normalized:
            return "frontend developer"
        elif "backend" in normalized or "back-end" in normalized:
            return "backend developer"
        elif "data scientist" in normalized:
            return "data scientist"
        elif "data analyst" in normalized:
            return "data analyst"
        elif "ux" in normalized or "user experience" in normalized:
            return "ux designer"
        elif "graphic" in normalized and "designer" in normalized:
            return "graphic designer"
        elif "sales" in normalized:
            return "sales representative"
        elif "attorney" in normalized or "lawyer" in normalized:
            return "attorney"
        elif "nurse" in normalized:
            return "nurse"
        elif "financial" in normalized and "analyst" in normalized:
            return "financial analyst"
        elif "customer service" in normalized or "customer support" in normalized:
            return "customer service"
        elif "administrative" in normalized or "admin" in normalized:
            return "administrative assistant"
        elif "receptionist" in normalized:
            return "receptionist"
        
        return normalized
    
    def _create_job_url(self, source: str, job_title: str, location: str) -> str:
        """Create realistic job search URL"""
        query = job_title.replace(' ', '+')
        location_formatted = location.replace(' ', '+').replace(',', '%2C')
        
        if source == "Indeed":
            return f"https://www.indeed.com/jobs?q={query}&l={location_formatted}&fromage=7"
        elif source == "LinkedIn":
            return f"https://www.linkedin.com/jobs/search/?keywords={query.replace('+', '%20')}&location={location_formatted.replace('+', '%20')}&f_TPR=r604800"
        elif source == "Glassdoor":
            return f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query.replace('+', '-')}&locT=C&locId=&jobType=&fromAge=7"
        elif source == "Handshake":
            return f"https://www.handshake.com/jobs/search?query={query.replace('+', '%20')}&location={location_formatted.replace('+', '%20')}"
        elif source == "County Jobs":
            return f"https://countyjobs.com/search?q={query.replace('+', '-')}&location={location_formatted.replace('+', '%20')}"
        
        return f"https://www.indeed.com/jobs?q={query}&l={location_formatted}&fromage=7"
    
    async def generate_realistic_jobs(self, job_title: str, location: str = "", limit: int = 1000) -> List[JobListing]:
        """Generate realistic jobs that actually match the search query"""
        
        # Normalize the job title
        normalized_title = self._normalize_job_title(job_title)
        
        # Check if we have mapping for this job type
        if normalized_title not in self.job_mappings:
            self.logger.warning(f"No realistic mapping found for job title: {job_title}")
            return []
        
        job_config = self.job_mappings[normalized_title]
        
        # For receptionist and some other roles, return limited results
        if normalized_title == "receptionist":
            self.logger.info(f"Receptionist roles are typically not posted by major companies on job platforms")
            return []
        
        jobs = []
        sources = ["Indeed", "LinkedIn", "Glassdoor", "Handshake", "County Jobs"]
        
        # Generate jobs across different sources
        jobs_per_source = max(1, limit // len(sources))
        
        for source in sources:
            for i in range(jobs_per_source):
                # Choose experience level
                exp_level = random.choice(list(self.experience_levels.keys()))
                exp_config = self.experience_levels[exp_level]
                
                # Create job title variation
                if exp_config["prefix"]:
                    title = f"{exp_config['prefix']} {job_title}"
                else:
                    title = job_title
                
                # Select company
                company = random.choice(job_config["companies"])
                
                # Select location
                if location:
                    job_location = location
                else:
                    job_location = random.choice(job_config["locations"])
                
                # Calculate salary
                base_min, base_max = job_config["salary_range"]
                salary_min = int(base_min * exp_config["multiplier"])
                salary_max = int(base_max * exp_config["multiplier"])
                
                # Determine remote work
                is_remote = job_config["remote_friendly"] and (job_location == "Remote" or random.random() < 0.3)
                
                # Create job URL
                apply_url = self._create_job_url(source, title, job_location)
                
                # Create job description
                description = f"We are seeking a qualified {title} to join our team at {company}. This role offers competitive compensation and growth opportunities in {job_location}."
                
                # Calculate match score
                match_score = random.randint(75, 95)
                
                # Select skills
                skills = random.sample(job_config["skills"], min(5, len(job_config["skills"])))
                
                # Create job listing
                job = JobListing(
                    title=title,
                    company=company,
                    location=job_location,
                    description=description,
                    salary=f"${salary_min//1000}K - ${salary_max//1000}K",
                    employment_type="Full-time",
                    posted_date=f"{random.randint(1, 7)} days ago",
                    apply_url=apply_url,
                    source=f"🔍 {source}",
                    skills=skills,
                    experience_level=exp_level.title(),
                    remote_work=is_remote,
                    match_score=match_score
                )
                jobs.append(job)
                
                if len(jobs) >= limit:
                    break
            
            if len(jobs) >= limit:
                break
        
        # Sort by match score
        jobs.sort(key=lambda x: x.match_score, reverse=True)
        
        self.logger.info(f"Generated {len(jobs)} realistic jobs for '{job_title}' (normalized: '{normalized_title}')")
        return jobs[:limit] 