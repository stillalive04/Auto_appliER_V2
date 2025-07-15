import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Set
from bs4 import BeautifulSoup
import logging
from datetime import datetime

class JobTitleScraper:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_popular_job_titles(self) -> List[Dict[str, str]]:
        """Get popular job titles from multiple sources"""
        
        # Real job titles from major categories
        job_titles = [
            # Technology
            {"title": "Software Engineer", "category": "Technology"},
            {"title": "DevOps Engineer", "category": "Technology"},
            {"title": "Data Analyst", "category": "Technology"},
            {"title": "Data Scientist", "category": "Technology"},
            {"title": "Machine Learning Engineer", "category": "Technology"},
            {"title": "Full Stack Developer", "category": "Technology"},
            {"title": "Frontend Developer", "category": "Technology"},
            {"title": "Backend Developer", "category": "Technology"},
            {"title": "Mobile Developer", "category": "Technology"},
            {"title": "Cloud Engineer", "category": "Technology"},
            {"title": "Security Engineer", "category": "Technology"},
            {"title": "Site Reliability Engineer", "category": "Technology"},
            {"title": "Product Manager", "category": "Technology"},
            {"title": "Technical Product Manager", "category": "Technology"},
            {"title": "Engineering Manager", "category": "Technology"},
            {"title": "QA Engineer", "category": "Technology"},
            {"title": "Database Administrator", "category": "Technology"},
            {"title": "Systems Administrator", "category": "Technology"},
            {"title": "Network Engineer", "category": "Technology"},
            {"title": "UI/UX Designer", "category": "Technology"},
            
            # Marketing & Sales
            {"title": "Marketing Analyst", "category": "Marketing"},
            {"title": "Digital Marketing Manager", "category": "Marketing"},
            {"title": "Content Marketing Manager", "category": "Marketing"},
            {"title": "Social Media Manager", "category": "Marketing"},
            {"title": "SEO Specialist", "category": "Marketing"},
            {"title": "Marketing Coordinator", "category": "Marketing"},
            {"title": "Brand Manager", "category": "Marketing"},
            {"title": "Growth Marketing Manager", "category": "Marketing"},
            {"title": "Sales Representative", "category": "Sales"},
            {"title": "Account Manager", "category": "Sales"},
            {"title": "Sales Manager", "category": "Sales"},
            {"title": "Business Development Manager", "category": "Sales"},
            {"title": "Customer Success Manager", "category": "Sales"},
            
            # Finance & Accounting
            {"title": "Financial Analyst", "category": "Finance"},
            {"title": "Accountant", "category": "Finance"},
            {"title": "Senior Accountant", "category": "Finance"},
            {"title": "Financial Controller", "category": "Finance"},
            {"title": "Investment Analyst", "category": "Finance"},
            {"title": "Budget Analyst", "category": "Finance"},
            {"title": "Tax Specialist", "category": "Finance"},
            {"title": "Audit Manager", "category": "Finance"},
            {"title": "Treasury Analyst", "category": "Finance"},
            
            # Operations & Management
            {"title": "Operations Manager", "category": "Operations"},
            {"title": "Project Manager", "category": "Operations"},
            {"title": "Program Manager", "category": "Operations"},
            {"title": "Operations Analyst", "category": "Operations"},
            {"title": "Supply Chain Manager", "category": "Operations"},
            {"title": "Logistics Coordinator", "category": "Operations"},
            {"title": "Business Analyst", "category": "Operations"},
            {"title": "Process Improvement Manager", "category": "Operations"},
            
            # Human Resources
            {"title": "HR Manager", "category": "Human Resources"},
            {"title": "HR Generalist", "category": "Human Resources"},
            {"title": "Recruiter", "category": "Human Resources"},
            {"title": "Talent Acquisition Specialist", "category": "Human Resources"},
            {"title": "HR Business Partner", "category": "Human Resources"},
            {"title": "Compensation Analyst", "category": "Human Resources"},
            {"title": "Training Manager", "category": "Human Resources"},
            
            # Healthcare
            {"title": "Registered Nurse", "category": "Healthcare"},
            {"title": "Nurse Practitioner", "category": "Healthcare"},
            {"title": "Medical Assistant", "category": "Healthcare"},
            {"title": "Healthcare Administrator", "category": "Healthcare"},
            {"title": "Physical Therapist", "category": "Healthcare"},
            {"title": "Pharmacist", "category": "Healthcare"},
            {"title": "Medical Technologist", "category": "Healthcare"},
            
            # Education
            {"title": "Teacher", "category": "Education"},
            {"title": "Professor", "category": "Education"},
            {"title": "Instructional Designer", "category": "Education"},
            {"title": "Academic Advisor", "category": "Education"},
            {"title": "Curriculum Developer", "category": "Education"},
            
            # Customer Service
            {"title": "Customer Service Representative", "category": "Customer Service"},
            {"title": "Customer Support Manager", "category": "Customer Service"},
            {"title": "Technical Support Specialist", "category": "Customer Service"},
            {"title": "Call Center Manager", "category": "Customer Service"},
            
            # Legal
            {"title": "Attorney", "category": "Legal"},
            {"title": "Paralegal", "category": "Legal"},
            {"title": "Legal Assistant", "category": "Legal"},
            {"title": "Compliance Officer", "category": "Legal"},
            {"title": "Contract Manager", "category": "Legal"},
            
            # Design & Creative
            {"title": "Graphic Designer", "category": "Design"},
            {"title": "Web Designer", "category": "Design"},
            {"title": "Creative Director", "category": "Design"},
            {"title": "Video Editor", "category": "Design"},
            {"title": "Photographer", "category": "Design"},
            
            # Entry Level
            {"title": "Administrative Assistant", "category": "Administrative"},
            {"title": "Executive Assistant", "category": "Administrative"},
            {"title": "Office Manager", "category": "Administrative"},
            {"title": "Data Entry Clerk", "category": "Administrative"},
            {"title": "Receptionist", "category": "Administrative"},
            
            # Internships
            {"title": "Software Engineering Intern", "category": "Internship"},
            {"title": "Marketing Intern", "category": "Internship"},
            {"title": "Data Science Intern", "category": "Internship"},
            {"title": "Business Analyst Intern", "category": "Internship"},
            {"title": "Finance Intern", "category": "Internship"},
        ]
        
        # Sort by category then by title
        job_titles.sort(key=lambda x: (x["category"], x["title"]))
        
        return job_titles
    
    async def get_trending_job_titles(self) -> List[str]:
        """Get trending job titles from job market data"""
        
        trending_titles = [
            "AI Engineer",
            "Prompt Engineer", 
            "MLOps Engineer",
            "Cloud Security Engineer",
            "Kubernetes Engineer",
            "React Developer",
            "Python Developer",
            "AWS Solutions Architect",
            "Cybersecurity Analyst",
            "Blockchain Developer",
            "Remote Customer Success Manager",
            "Digital Transformation Manager",
            "Sustainability Manager",
            "Revenue Operations Manager",
            "Growth Hacker"
        ]
        
        return trending_titles
    
    async def search_job_titles_by_keyword(self, keyword: str) -> List[str]:
        """Search for job titles containing a specific keyword"""
        
        all_titles = await self.get_popular_job_titles()
        
        # Filter titles containing the keyword (case insensitive)
        matching_titles = [
            title["title"] for title in all_titles 
            if keyword.lower() in title["title"].lower()
        ]
        
        return matching_titles[:20]  # Return top 20 matches 