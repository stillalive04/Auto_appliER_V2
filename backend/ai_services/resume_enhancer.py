import logging
from typing import Dict, List
from ai_services.custom_ai_engine import CustomAIEngine

class ResumeEnhancer:
    def __init__(self):
        self.custom_ai = CustomAIEngine()
        self.logger = logging.getLogger(__name__)
        
    def enhance_resume_for_job(self, resume_text: str, job_description: str) -> Dict:
        """Enhance resume based on job description using custom AI engine"""
        try:
            return self.custom_ai.enhance_resume_for_job(resume_text, job_description)
        except Exception as e:
            self.logger.error(f"Error enhancing resume: {e}")
            return {
                "enhanced_resume": resume_text,
                "improvements": [],
                "keywords_added": [],
                "match_score": 0.3
            }
    
    def analyze_resume_quality(self, resume_text: str) -> Dict:
        """Analyze resume quality and provide suggestions"""
        try:
            # Parse resume using custom AI
            resume_data = self.custom_ai.parse_resume(resume_text)
            
            # Analyze quality
            quality_score = 0.0
            suggestions = []
            
            # Check for contact information
            if resume_data.get('contact'):
                quality_score += 0.2
            else:
                suggestions.append("Add contact information (email, phone)")
            
            # Check for summary/objective
            if resume_data.get('summary') and len(resume_data['summary']) > 50:
                quality_score += 0.2
            else:
                suggestions.append("Add a professional summary or objective")
            
            # Check for skills section
            if resume_data.get('skills') and len(resume_data['skills']) > 3:
                quality_score += 0.2
            else:
                suggestions.append("Add a comprehensive skills section")
            
            # Check for experience
            if resume_data.get('experience') and len(resume_data['experience']) > 0:
                quality_score += 0.2
            else:
                suggestions.append("Add professional experience details")
            
            # Check for education
            if resume_data.get('education'):
                quality_score += 0.1
            else:
                suggestions.append("Add education information")
            
            # Check for quantified achievements
            resume_text_lower = resume_text.lower()
            if any(char in resume_text_lower for char in ['%', '$', '+']):
                quality_score += 0.1
            else:
                suggestions.append("Add quantified achievements and results")
            
            return {
                "quality_score": min(1.0, quality_score),
                "suggestions": suggestions,
                "word_count": len(resume_text.split()),
                "sections_found": list(resume_data.keys())
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing resume quality: {e}")
            return {
                "quality_score": 0.5,
                "suggestions": ["Unable to analyze resume quality"],
                "word_count": len(resume_text.split()),
                "sections_found": []
            }
    
    def get_ats_optimization_score(self, resume_text: str) -> Dict:
        """Calculate ATS (Applicant Tracking System) optimization score"""
        try:
            score = 0.0
            issues = []
            
            # Check for proper formatting
            if '\n' in resume_text:
                score += 0.2
            else:
                issues.append("Use proper line breaks and formatting")
            
            # Check for standard section headers
            standard_headers = ['experience', 'education', 'skills', 'summary', 'objective']
            found_headers = sum(1 for header in standard_headers if header in resume_text.lower())
            score += min(0.3, found_headers * 0.1)
            
            if found_headers < 3:
                issues.append("Use standard section headers (Experience, Education, Skills)")
            
            # Check for keywords density
            words = resume_text.split()
            if len(words) > 200:
                score += 0.2
            else:
                issues.append("Resume should be more detailed (aim for 300-500 words)")
            
            # Check for contact information
            if '@' in resume_text:
                score += 0.1
            else:
                issues.append("Include email address")
            
            # Check for dates
            import re
            date_pattern = r'\b\d{4}\b|\b\d{1,2}/\d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b'
            if re.search(date_pattern, resume_text):
                score += 0.1
            else:
                issues.append("Include dates for experience and education")
            
            # Check for bullet points or structured format
            if '•' in resume_text or '-' in resume_text:
                score += 0.1
            else:
                issues.append("Use bullet points for better readability")
            
            return {
                "ats_score": min(1.0, score),
                "optimization_issues": issues,
                "is_ats_friendly": score > 0.7
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating ATS score: {e}")
            return {
                "ats_score": 0.5,
                "optimization_issues": ["Unable to analyze ATS compatibility"],
                "is_ats_friendly": False
            } 