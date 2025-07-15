import re
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

class CustomAIEngine:
    """
    Custom AI Engine for job application automation
    - Enhances resumes based on job descriptions
    - Generates personalized cover letters
    - Creates PDF documents
    - Learns from newspaper job postings
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Knowledge base for job matching
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'react', 'node.js', 'sql', 'html', 'css', 'git'],
            'data_science': ['machine learning', 'data analysis', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'r'],
            'web_development': ['react', 'angular', 'vue', 'express', 'django', 'flask', 'rest api', 'graphql'],
            'mobile': ['react native', 'flutter', 'ios', 'android', 'swift', 'kotlin'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'jenkins', 'ci/cd', 'terraform'],
            'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'soft_skills': ['communication', 'teamwork', 'leadership', 'problem solving', 'agile', 'scrum']
        }
        
        # Job title patterns
        self.job_title_patterns = {
            'software_engineer': ['software engineer', 'developer', 'programmer', 'software developer'],
            'data_scientist': ['data scientist', 'data analyst', 'machine learning engineer'],
            'frontend_developer': ['frontend developer', 'front-end developer', 'ui developer'],
            'backend_developer': ['backend developer', 'back-end developer', 'server developer'],
            'full_stack': ['full stack developer', 'full-stack developer', 'fullstack developer'],
            'devops_engineer': ['devops engineer', 'site reliability engineer', 'infrastructure engineer'],
            'product_manager': ['product manager', 'product owner', 'project manager']
        }
        
        # Industry-specific knowledge
        self.industry_knowledge = {
            'fintech': ['financial services', 'banking', 'payments', 'cryptocurrency', 'blockchain'],
            'healthcare': ['healthcare', 'medical', 'telemedicine', 'health tech', 'pharma'],
            'ecommerce': ['e-commerce', 'retail', 'online shopping', 'marketplace'],
            'edtech': ['education', 'learning', 'online courses', 'educational technology'],
            'gaming': ['gaming', 'game development', 'entertainment', 'mobile games'],
            'enterprise': ['enterprise software', 'b2b', 'saas', 'business solutions']
        }
        
        # Resume templates
        self.resume_templates = {
            'technical': {
                'sections': ['Contact', 'Professional Summary', 'Technical Skills', 'Experience', 'Education', 'Projects'],
                'emphasis': 'technical_skills'
            },
            'managerial': {
                'sections': ['Contact', 'Executive Summary', 'Core Competencies', 'Professional Experience', 'Education', 'Achievements'],
                'emphasis': 'leadership'
            },
            'entry_level': {
                'sections': ['Contact', 'Objective', 'Education', 'Skills', 'Projects', 'Experience'],
                'emphasis': 'education_projects'
            }
        }

    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description to extract key requirements and skills"""
        try:
            job_description = job_description.lower()
            
            # Extract required skills
            required_skills = []
            for category, skills in self.skill_keywords.items():
                found_skills = [skill for skill in skills if skill in job_description]
                if found_skills:
                    required_skills.extend(found_skills)
            
            # Determine job type
            job_type = 'general'
            for job_category, patterns in self.job_title_patterns.items():
                if any(pattern in job_description for pattern in patterns):
                    job_type = job_category
                    break
            
            # Determine industry
            industry = 'general'
            for industry_name, keywords in self.industry_knowledge.items():
                if any(keyword in job_description for keyword in keywords):
                    industry = industry_name
                    break
            
            # Extract experience requirements
            experience_match = re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?experience', job_description)
            required_experience = int(experience_match.group(1)) if experience_match else 2
            
            # Extract education requirements
            education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
            requires_degree = any(keyword in job_description for keyword in education_keywords)
            
            # Extract salary information
            salary_match = re.search(r'\$(\d+,?\d*)\s*-?\s*\$?(\d+,?\d*)?', job_description)
            salary_range = None
            if salary_match:
                min_salary = salary_match.group(1).replace(',', '')
                max_salary = salary_match.group(2).replace(',', '') if salary_match.group(2) else min_salary
                salary_range = {'min': int(min_salary), 'max': int(max_salary)}
            
            return {
                'required_skills': required_skills,
                'job_type': job_type,
                'industry': industry,
                'required_experience': required_experience,
                'requires_degree': requires_degree,
                'salary_range': salary_range,
                'match_score': len(required_skills) / 10  # Simple scoring
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing job description: {e}")
            return {'required_skills': [], 'job_type': 'general', 'industry': 'general', 'match_score': 0.5}

    def enhance_resume_for_job(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Enhance resume based on job description analysis"""
        try:
            job_analysis = self.analyze_job_description(job_description)
            
            # Parse existing resume
            resume_data = self.parse_resume(resume_text)
            
            # Enhance resume based on job requirements
            enhanced_resume = self.optimize_resume_content(resume_data, job_analysis)
            
            # Generate PDF
            pdf_content = self.generate_resume_pdf(enhanced_resume)
            
            return {
                'enhanced_resume': enhanced_resume,
                'pdf_content': pdf_content,
                'match_score': job_analysis['match_score'],
                'improvements': self.suggest_improvements(resume_data, job_analysis),
                'missing_skills': self.identify_missing_skills(resume_data, job_analysis)
            }
            
        except Exception as e:
            self.logger.error(f"Error enhancing resume: {e}")
            return {'enhanced_resume': resume_text, 'match_score': 0.5, 'improvements': []}

    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Parse resume text into structured data"""
        try:
            # Simple parsing - in production, use more sophisticated NLP
            lines = resume_text.split('\n')
            
            resume_data = {
                'contact': {},
                'summary': '',
                'experience': [],
                'education': [],
                'skills': [],
                'projects': []
            }
            
            current_section = None
            current_content = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ['experience', 'work history', 'employment']):
                    current_section = 'experience'
                elif any(keyword in line_lower for keyword in ['education', 'academic', 'qualification']):
                    current_section = 'education'
                elif any(keyword in line_lower for keyword in ['skills', 'technical skills', 'competencies']):
                    current_section = 'skills'
                elif any(keyword in line_lower for keyword in ['projects', 'portfolio']):
                    current_section = 'projects'
                elif any(keyword in line_lower for keyword in ['summary', 'objective', 'profile']):
                    current_section = 'summary'
                elif '@' in line or 'phone' in line_lower or 'email' in line_lower:
                    current_section = 'contact'
                
                # Add content to current section
                if current_section:
                    if current_section == 'summary':
                        resume_data['summary'] += line + ' '
                    elif current_section == 'contact':
                        if '@' in line:
                            resume_data['contact']['email'] = line
                        elif any(char.isdigit() for char in line):
                            resume_data['contact']['phone'] = line
                    elif current_section == 'skills':
                        # Extract skills from line
                        skills = [skill.strip() for skill in line.split(',') if skill.strip()]
                        resume_data['skills'].extend(skills)
                    else:
                        current_content.append(line)
                        if current_section in ['experience', 'education', 'projects']:
                            resume_data[current_section].append(line)
            
            return resume_data
            
        except Exception as e:
            self.logger.error(f"Error parsing resume: {e}")
            return {'contact': {}, 'summary': resume_text[:200], 'experience': [], 'skills': []}

    def optimize_resume_content(self, resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Optimize resume content based on job analysis"""
        try:
            optimized = resume_data.copy()
            
            # Enhance summary with job-relevant keywords
            if job_analysis['required_skills']:
                relevant_skills = [skill for skill in job_analysis['required_skills'] 
                                 if skill in optimized.get('summary', '').lower()]
                if len(relevant_skills) < 3:
                    # Add missing relevant skills to summary
                    missing_skills = job_analysis['required_skills'][:3]
                    optimized['summary'] += f" Experienced with {', '.join(missing_skills)}."
            
            # Reorder skills to prioritize job-relevant ones
            if optimized.get('skills'):
                job_skills = job_analysis['required_skills']
                prioritized_skills = []
                
                # Add matching skills first
                for skill in optimized['skills']:
                    if any(job_skill in skill.lower() for job_skill in job_skills):
                        prioritized_skills.append(skill)
                
                # Add remaining skills
                for skill in optimized['skills']:
                    if skill not in prioritized_skills:
                        prioritized_skills.append(skill)
                
                optimized['skills'] = prioritized_skills
            
            # Add industry-specific keywords
            if job_analysis['industry'] != 'general':
                industry_keywords = self.industry_knowledge.get(job_analysis['industry'], [])
                optimized['industry_focus'] = industry_keywords[:3]
            
            return optimized
            
        except Exception as e:
            self.logger.error(f"Error optimizing resume: {e}")
            return resume_data

    def generate_cover_letter(self, job_data: Dict, user_profile: Dict, enhanced_resume: Dict) -> Dict[str, Any]:
        """Generate personalized cover letter"""
        try:
            company_name = job_data.get('company', 'the company')
            job_title = job_data.get('title', 'the position')
            user_name = user_profile.get('full_name', 'John Doe')
            
            # Generate cover letter content
            cover_letter_content = self.create_cover_letter_content(
                user_name, company_name, job_title, job_data, enhanced_resume
            )
            
            # Generate PDF
            pdf_content = self.generate_cover_letter_pdf(cover_letter_content, user_profile)
            
            return {
                'cover_letter': cover_letter_content,
                'pdf_content': pdf_content,
                'personalization_score': self.calculate_personalization_score(cover_letter_content, job_data)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter: {e}")
            return {'cover_letter': 'Generic cover letter', 'personalization_score': 0.5}

    def create_cover_letter_content(self, user_name: str, company_name: str, job_title: str, 
                                  job_data: Dict, enhanced_resume: Dict) -> str:
        """Create cover letter content"""
        try:
            # Extract key skills from resume
            skills = enhanced_resume.get('skills', [])[:3]
            skills_text = ', '.join(skills) if skills else 'various technical skills'
            
            # Create personalized content
            cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in {skills_text}, I am confident that I would be a valuable addition to your team.

In my previous roles, I have successfully developed and implemented solutions that align with the requirements outlined in your job posting. My experience with {skills_text} has prepared me to tackle the challenges and contribute to {company_name}'s continued success.

What particularly excites me about this opportunity at {company_name} is the chance to work on innovative projects and contribute to a team that values excellence and growth. I am eager to bring my technical expertise and problem-solving abilities to help drive your company's objectives forward.

I would welcome the opportunity to discuss how my skills and experience can contribute to your team's success. Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
{user_name}"""
            
            return cover_letter
            
        except Exception as e:
            self.logger.error(f"Error creating cover letter content: {e}")
            return f"Dear Hiring Manager,\n\nI am interested in the {job_title} position at {company_name}.\n\nSincerely,\n{user_name}"

    def generate_resume_pdf(self, resume_data: Dict) -> str:
        """Generate PDF resume and return as base64 string"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Build PDF content
            story = []
            
            # Title
            story.append(Paragraph("Resume", title_style))
            story.append(Spacer(1, 12))
            
            # Contact Information
            if resume_data.get('contact'):
                contact = resume_data['contact']
                contact_text = f"Email: {contact.get('email', 'N/A')} | Phone: {contact.get('phone', 'N/A')}"
                story.append(Paragraph(contact_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Summary
            if resume_data.get('summary'):
                story.append(Paragraph("Professional Summary", heading_style))
                story.append(Paragraph(resume_data['summary'], styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Skills
            if resume_data.get('skills'):
                story.append(Paragraph("Technical Skills", heading_style))
                skills_text = ', '.join(resume_data['skills'])
                story.append(Paragraph(skills_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Experience
            if resume_data.get('experience'):
                story.append(Paragraph("Professional Experience", heading_style))
                for exp in resume_data['experience']:
                    story.append(Paragraph(f"• {exp}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Education
            if resume_data.get('education'):
                story.append(Paragraph("Education", heading_style))
                for edu in resume_data['education']:
                    story.append(Paragraph(f"• {edu}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Projects
            if resume_data.get('projects'):
                story.append(Paragraph("Projects", heading_style))
                for project in resume_data['projects']:
                    story.append(Paragraph(f"• {project}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            # Convert to base64
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return base64.b64encode(pdf_data).decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Error generating resume PDF: {e}")
            return ""

    def generate_cover_letter_pdf(self, cover_letter_content: str, user_profile: Dict) -> str:
        """Generate PDF cover letter and return as base64 string"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            # Define styles
            styles = getSampleStyleSheet()
            
            # Build PDF content
            story = []
            
            # Header with user info
            user_name = user_profile.get('full_name', 'John Doe')
            user_email = user_profile.get('email', 'john@example.com')
            user_phone = user_profile.get('phone', '(555) 123-4567')
            
            header_text = f"{user_name}<br/>{user_email}<br/>{user_phone}"
            story.append(Paragraph(header_text, styles['Normal']))
            story.append(Spacer(1, 24))
            
            # Date
            current_date = datetime.now().strftime("%B %d, %Y")
            story.append(Paragraph(current_date, styles['Normal']))
            story.append(Spacer(1, 24))
            
            # Cover letter content
            paragraphs = cover_letter_content.split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    story.append(Paragraph(paragraph.strip(), styles['Normal']))
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            # Convert to base64
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return base64.b64encode(pdf_data).decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter PDF: {e}")
            return ""

    def learn_from_newspaper_jobs(self, newspaper_jobs: List[Dict]) -> Dict[str, Any]:
        """Learn patterns from newspaper job postings to improve AI"""
        try:
            if not newspaper_jobs:
                return {'learned_patterns': [], 'skill_frequency': {}}
            
            # Analyze job patterns
            skill_frequency = {}
            industry_patterns = {}
            salary_patterns = {}
            
            for job in newspaper_jobs:
                # Extract skills from job descriptions
                description = job.get('description', '').lower()
                for category, skills in self.skill_keywords.items():
                    for skill in skills:
                        if skill in description:
                            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
                
                # Track industry patterns
                industry = job.get('industry', 'general')
                industry_patterns[industry] = industry_patterns.get(industry, 0) + 1
                
                # Track salary patterns
                salary = job.get('salary', '')
                if salary:
                    salary_patterns[salary] = salary_patterns.get(salary, 0) + 1
            
            # Update knowledge base with learned patterns
            self.update_knowledge_base(skill_frequency, industry_patterns)
            
            return {
                'learned_patterns': list(skill_frequency.keys()),
                'skill_frequency': skill_frequency,
                'industry_trends': industry_patterns,
                'total_jobs_analyzed': len(newspaper_jobs)
            }
            
        except Exception as e:
            self.logger.error(f"Error learning from newspaper jobs: {e}")
            return {'learned_patterns': [], 'skill_frequency': {}}

    def update_knowledge_base(self, skill_frequency: Dict, industry_patterns: Dict):
        """Update internal knowledge base with learned patterns"""
        try:
            # Update skill keywords with frequently mentioned skills
            for skill, frequency in skill_frequency.items():
                if frequency > 5:  # Threshold for adding to knowledge base
                    # Find appropriate category
                    for category, skills in self.skill_keywords.items():
                        if skill in skills:
                            continue
                        # Add to most relevant category (simplified logic)
                        if any(related in skill for related in ['python', 'java', 'javascript']):
                            self.skill_keywords['programming'].append(skill)
                            break
            
            self.logger.info(f"Updated knowledge base with {len(skill_frequency)} skills")
            
        except Exception as e:
            self.logger.error(f"Error updating knowledge base: {e}")

    def suggest_improvements(self, resume_data: Dict, job_analysis: Dict) -> List[str]:
        """Suggest improvements for resume based on job analysis"""
        suggestions = []
        
        try:
            # Check for missing skills
            required_skills = job_analysis.get('required_skills', [])
            resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
            
            missing_skills = [skill for skill in required_skills if skill not in resume_skills]
            if missing_skills:
                suggestions.append(f"Consider adding these skills: {', '.join(missing_skills[:3])}")
            
            # Check summary length
            summary = resume_data.get('summary', '')
            if len(summary) < 100:
                suggestions.append("Consider expanding your professional summary")
            
            # Check for quantified achievements
            experience_text = ' '.join(resume_data.get('experience', []))
            if not re.search(r'\d+%|\d+\+|\$\d+', experience_text):
                suggestions.append("Add quantified achievements to your experience section")
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error suggesting improvements: {e}")
            return ["Consider reviewing and updating your resume"]

    def identify_missing_skills(self, resume_data: Dict, job_analysis: Dict) -> List[str]:
        """Identify skills missing from resume that are required for job"""
        try:
            required_skills = job_analysis.get('required_skills', [])
            resume_text = ' '.join([
                resume_data.get('summary', ''),
                ' '.join(resume_data.get('skills', [])),
                ' '.join(resume_data.get('experience', []))
            ]).lower()
            
            missing_skills = []
            for skill in required_skills:
                if skill not in resume_text:
                    missing_skills.append(skill)
            
            return missing_skills[:5]  # Return top 5 missing skills
            
        except Exception as e:
            self.logger.error(f"Error identifying missing skills: {e}")
            return []

    def calculate_personalization_score(self, cover_letter: str, job_data: Dict) -> float:
        """Calculate how personalized the cover letter is"""
        try:
            score = 0.0
            
            # Check for company name
            if job_data.get('company', '').lower() in cover_letter.lower():
                score += 0.3
            
            # Check for job title
            if job_data.get('title', '').lower() in cover_letter.lower():
                score += 0.3
            
            # Check for specific skills mentioned
            job_description = job_data.get('description', '').lower()
            cover_letter_lower = cover_letter.lower()
            
            skill_matches = 0
            for category, skills in self.skill_keywords.items():
                for skill in skills:
                    if skill in job_description and skill in cover_letter_lower:
                        skill_matches += 1
            
            if skill_matches > 0:
                score += min(0.4, skill_matches * 0.1)
            
            return min(1.0, score)
            
        except Exception as e:
            self.logger.error(f"Error calculating personalization score: {e}")
            return 0.5 