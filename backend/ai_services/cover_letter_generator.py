import logging
from typing import Dict, List
from ai_services.custom_ai_engine import CustomAIEngine

class CoverLetterGenerator:
    def __init__(self):
        self.custom_ai = CustomAIEngine()
        self.logger = logging.getLogger(__name__)
    
    def generate_cover_letter(self, job_data: Dict, user_profile: Dict, enhanced_resume: Dict) -> Dict:
        """Generate personalized cover letter using custom AI engine"""
        try:
            return self.custom_ai.generate_cover_letter(job_data, user_profile, enhanced_resume)
        except Exception as e:
            self.logger.error(f"Error generating cover letter: {e}")
            return {
                'cover_letter': self.generate_fallback_cover_letter(job_data, user_profile),
                'personalization_score': 0.3
            }
    
    def generate_fallback_cover_letter(self, job_data: Dict, user_profile: Dict) -> str:
        """Generate a basic cover letter as fallback"""
        try:
            company_name = job_data.get('company', 'the company')
            job_title = job_data.get('title', 'the position')
            user_name = user_profile.get('full_name', 'John Doe')
            
            return f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company_name}. With my background in technology and software development, I am confident that I would be a valuable addition to your team.

My experience has prepared me to tackle the challenges outlined in your job posting. I am particularly excited about the opportunity to contribute to {company_name}'s mission and work with a team that values innovation and excellence.

I would welcome the opportunity to discuss how my skills and experience can contribute to your team's success. Thank you for considering my application.

Sincerely,
{user_name}"""
        
        except Exception as e:
            self.logger.error(f"Error generating fallback cover letter: {e}")
            return "Dear Hiring Manager,\n\nI am interested in this position.\n\nSincerely,\nApplicant"
    
    def analyze_cover_letter_quality(self, cover_letter: str, job_data: Dict) -> Dict:
        """Analyze the quality of a cover letter"""
        try:
            quality_score = 0.0
            suggestions = []
            
            # Check length
            word_count = len(cover_letter.split())
            if 150 <= word_count <= 400:
                quality_score += 0.2
            else:
                suggestions.append("Cover letter should be 150-400 words")
            
            # Check for company name
            company_name = job_data.get('company', '').lower()
            if company_name and company_name in cover_letter.lower():
                quality_score += 0.2
            else:
                suggestions.append("Include the company name")
            
            # Check for job title
            job_title = job_data.get('title', '').lower()
            if job_title and job_title in cover_letter.lower():
                quality_score += 0.2
            else:
                suggestions.append("Reference the specific job title")
            
            # Check for personalization
            personal_pronouns = ['i', 'my', 'me']
            pronoun_count = sum(1 for word in cover_letter.lower().split() if word in personal_pronouns)
            if pronoun_count >= 5:
                quality_score += 0.2
            else:
                suggestions.append("Make the letter more personal")
            
            # Check for action words
            action_words = ['developed', 'managed', 'led', 'created', 'implemented', 'achieved']
            action_count = sum(1 for word in action_words if word in cover_letter.lower())
            if action_count >= 2:
                quality_score += 0.1
            else:
                suggestions.append("Include more action words and achievements")
            
            # Check for proper structure
            if 'dear' in cover_letter.lower() and 'sincerely' in cover_letter.lower():
                quality_score += 0.1
            else:
                suggestions.append("Use proper business letter format")
            
            return {
                "quality_score": min(1.0, quality_score),
                "suggestions": suggestions,
                "word_count": word_count,
                "personalization_score": self.custom_ai.calculate_personalization_score(cover_letter, job_data)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing cover letter quality: {e}")
            return {
                "quality_score": 0.5,
                "suggestions": ["Unable to analyze cover letter quality"],
                "word_count": len(cover_letter.split()),
                "personalization_score": 0.5
            }
    
    def generate_multiple_versions(self, job_data: Dict, user_profile: Dict, enhanced_resume: Dict, count: int = 3) -> List[Dict]:
        """Generate multiple versions of cover letters"""
        try:
            versions = []
            
            for i in range(count):
                # Generate different styles
                if i == 0:
                    # Professional and formal
                    style = "professional"
                elif i == 1:
                    # Enthusiastic and energetic
                    style = "enthusiastic"
                else:
                    # Concise and direct
                    style = "concise"
                
                cover_letter_data = self.generate_cover_letter_with_style(job_data, user_profile, enhanced_resume, style)
                cover_letter_data['style'] = style
                versions.append(cover_letter_data)
            
            return versions
            
        except Exception as e:
            self.logger.error(f"Error generating multiple versions: {e}")
            return [self.generate_cover_letter(job_data, user_profile, enhanced_resume)]
    
    def generate_cover_letter_with_style(self, job_data: Dict, user_profile: Dict, enhanced_resume: Dict, style: str) -> Dict:
        """Generate cover letter with specific style"""
        try:
            company_name = job_data.get('company', 'the company')
            job_title = job_data.get('title', 'the position')
            user_name = user_profile.get('full_name', 'John Doe')
            
            if style == "professional":
                cover_letter = f"""Dear Hiring Manager,

I am writing to formally express my interest in the {job_title} position at {company_name}. With my extensive background in software development and proven track record of delivering high-quality solutions, I am well-positioned to contribute to your team's continued success.

My professional experience has equipped me with the technical skills and business acumen necessary to excel in this role. I am particularly drawn to {company_name}'s commitment to innovation and would welcome the opportunity to contribute to your ongoing projects.

I would appreciate the opportunity to discuss how my qualifications align with your needs. Thank you for your consideration.

Respectfully,
{user_name}"""
            
            elif style == "enthusiastic":
                cover_letter = f"""Dear Hiring Team,

I am thrilled to apply for the {job_title} position at {company_name}! Your company's reputation for innovation and excellence has long impressed me, and I am excited about the possibility of contributing to your dynamic team.

My passion for technology and problem-solving, combined with my hands-on experience, makes me an ideal candidate for this role. I am particularly excited about the opportunity to work on challenging projects and collaborate with talented professionals at {company_name}.

I would love to discuss how my enthusiasm and skills can benefit your team. Thank you for considering my application!

Best regards,
{user_name}"""
            
            else:  # concise
                cover_letter = f"""Dear Hiring Manager,

I am applying for the {job_title} position at {company_name}. My background in software development and proven ability to deliver results make me a strong candidate for this role.

Key qualifications:
• Extensive experience in software development
• Strong problem-solving and analytical skills
• Proven track record of successful project delivery

I am interested in discussing how I can contribute to {company_name}'s success. Thank you for your consideration.

Sincerely,
{user_name}"""
            
            return {
                'cover_letter': cover_letter,
                'pdf_content': self.custom_ai.generate_cover_letter_pdf(cover_letter, user_profile),
                'personalization_score': self.custom_ai.calculate_personalization_score(cover_letter, job_data)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating styled cover letter: {e}")
            return self.generate_cover_letter(job_data, user_profile, enhanced_resume)
    
    def optimize_for_ats(self, cover_letter: str, job_data: Dict) -> Dict:
        """Optimize cover letter for ATS (Applicant Tracking System)"""
        try:
            # Extract keywords from job description
            job_description = job_data.get('description', '').lower()
            job_analysis = self.custom_ai.analyze_job_description(job_description)
            
            optimized_letter = cover_letter
            optimization_notes = []
            
            # Add relevant keywords naturally
            required_skills = job_analysis.get('required_skills', [])
            for skill in required_skills[:3]:  # Add top 3 skills
                if skill not in cover_letter.lower():
                    # Try to add skill naturally
                    if 'experience' in cover_letter.lower():
                        optimized_letter = optimized_letter.replace(
                            'experience',
                            f'experience with {skill}',
                            1
                        )
                        optimization_notes.append(f"Added keyword: {skill}")
            
            # Ensure proper formatting
            if not optimized_letter.startswith('Dear'):
                optimized_letter = 'Dear Hiring Manager,\n\n' + optimized_letter
                optimization_notes.append("Added proper greeting")
            
            if not optimized_letter.endswith('Sincerely,'):
                optimized_letter += '\n\nSincerely,\n[Your Name]'
                optimization_notes.append("Added proper closing")
            
            return {
                'optimized_cover_letter': optimized_letter,
                'optimization_notes': optimization_notes,
                'keywords_added': required_skills[:3],
                'ats_score': self.calculate_ats_score(optimized_letter)
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing for ATS: {e}")
            return {
                'optimized_cover_letter': cover_letter,
                'optimization_notes': [],
                'keywords_added': [],
                'ats_score': 0.5
            }
    
    def calculate_ats_score(self, cover_letter: str) -> float:
        """Calculate ATS compatibility score"""
        try:
            score = 0.0
            
            # Check for proper structure
            if 'dear' in cover_letter.lower():
                score += 0.2
            
            if any(closing in cover_letter.lower() for closing in ['sincerely', 'best regards', 'respectfully']):
                score += 0.2
            
            # Check for keywords density
            words = cover_letter.split()
            if len(words) > 100:
                score += 0.2
            
            # Check for action verbs
            action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 'achieved', 'improved']
            action_count = sum(1 for verb in action_verbs if verb in cover_letter.lower())
            if action_count >= 2:
                score += 0.2
            
            # Check for formatting
            if '\n' in cover_letter:
                score += 0.1
            
            # Check for specific details
            if any(detail in cover_letter.lower() for detail in ['experience', 'skills', 'background']):
                score += 0.1
            
            return min(1.0, score)
            
        except Exception as e:
            self.logger.error(f"Error calculating ATS score: {e}")
            return 0.5 