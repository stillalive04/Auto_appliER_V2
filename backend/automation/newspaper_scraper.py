import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
import random
from urllib.parse import urljoin, urlparse
import feedparser

class NewspaperJobScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Canadian newspapers
        self.canadian_sources = {
            'globe_and_mail': {
                'name': 'The Globe and Mail',
                'base_url': 'https://www.theglobeandmail.com',
                'job_sections': [
                    '/business/careers/',
                    '/business/technology/',
                    '/business/economy/'
                ],
                'rss_feeds': [
                    'https://www.theglobeandmail.com/arc/outboundfeeds/rss/category/business/?outputType=xml'
                ]
            },
            'toronto_star': {
                'name': 'Toronto Star',
                'base_url': 'https://www.thestar.com',
                'job_sections': [
                    '/business/careers/',
                    '/business/technology/',
                    '/business/economy/'
                ],
                'rss_feeds': [
                    'https://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.business.rss'
                ]
            },
            'national_post': {
                'name': 'National Post',
                'base_url': 'https://nationalpost.com',
                'job_sections': [
                    '/business/careers/',
                    '/business/technology/',
                    '/business/economy/'
                ],
                'rss_feeds': [
                    'https://nationalpost.com/category/business/feed'
                ]
            },
            'cbc_news': {
                'name': 'CBC News',
                'base_url': 'https://www.cbc.ca',
                'job_sections': [
                    '/news/business/',
                    '/news/technology/',
                    '/news/canada/'
                ],
                'rss_feeds': [
                    'https://www.cbc.ca/cmlink/rss-business'
                ]
            }
        }
        
        # US newspapers
        self.us_sources = {
            'new_york_times': {
                'name': 'The New York Times',
                'base_url': 'https://www.nytimes.com',
                'job_sections': [
                    '/section/business/',
                    '/section/technology/',
                    '/section/business/economy/'
                ],
                'rss_feeds': [
                    'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml'
                ]
            },
            'washington_post': {
                'name': 'The Washington Post',
                'base_url': 'https://www.washingtonpost.com',
                'job_sections': [
                    '/business/',
                    '/technology/',
                    '/business/economy/'
                ],
                'rss_feeds': [
                    'https://feeds.washingtonpost.com/rss/business'
                ]
            },
            'wall_street_journal': {
                'name': 'The Wall Street Journal',
                'base_url': 'https://www.wsj.com',
                'job_sections': [
                    '/news/business/',
                    '/news/technology/',
                    '/news/economy/'
                ],
                'rss_feeds': [
                    'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml'
                ]
            },
            'usa_today': {
                'name': 'USA Today',
                'base_url': 'https://www.usatoday.com',
                'job_sections': [
                    '/money/business/',
                    '/tech/',
                    '/money/economy/'
                ],
                'rss_feeds': [
                    'https://www.usatoday.com/rss/business/'
                ]
            },
            'chicago_tribune': {
                'name': 'Chicago Tribune',
                'base_url': 'https://www.chicagotribune.com',
                'job_sections': [
                    '/business/',
                    '/business/technology/',
                    '/business/careers/'
                ],
                'rss_feeds': [
                    'https://www.chicagotribune.com/arcio/rss/category/business/'
                ]
            },
            'los_angeles_times': {
                'name': 'Los Angeles Times',
                'base_url': 'https://www.latimes.com',
                'job_sections': [
                    '/business/',
                    '/business/technology/',
                    '/business/story/'
                ],
                'rss_feeds': [
                    'https://www.latimes.com/business/rss2.0.xml'
                ]
            }
        }
        
        # Job-related keywords to search for
        self.job_keywords = [
            'hiring', 'job', 'career', 'employment', 'position', 'vacancy', 'opening',
            'recruit', 'staff', 'work', 'opportunity', 'application', 'candidate',
            'software engineer', 'developer', 'programmer', 'data scientist',
            'product manager', 'marketing', 'sales', 'analyst', 'consultant',
            'manager', 'director', 'executive', 'specialist', 'coordinator',
            'remote work', 'work from home', 'telecommute', 'freelance',
            'startup', 'tech company', 'corporation', 'enterprise'
        ]
        
        # Company indicators
        self.company_indicators = [
            'company', 'corp', 'corporation', 'inc', 'incorporated', 'ltd', 'limited',
            'llc', 'startup', 'firm', 'enterprise', 'organization', 'business',
            'tech', 'technology', 'software', 'digital', 'solutions', 'services'
        ]

    def scrape_all_newspapers(self, country: str = 'both', max_articles: int = 100) -> List[Dict]:
        """
        Scrape job postings from all newspaper sources
        
        Args:
            country: 'canada', 'us', or 'both'
            max_articles: Maximum number of articles to process
            
        Returns:
            List of job postings found
        """
        all_jobs = []
        
        try:
            sources = {}
            if country in ['canada', 'both']:
                sources.update(self.canadian_sources)
            if country in ['us', 'both']:
                sources.update(self.us_sources)
            
            for source_key, source_config in sources.items():
                self.logger.info(f"Scraping {source_config['name']}...")
                
                # Scrape RSS feeds first (faster)
                rss_jobs = self.scrape_rss_feeds(source_config)
                all_jobs.extend(rss_jobs)
                
                # Scrape web pages for more detailed job postings
                web_jobs = self.scrape_web_sections(source_config)
                all_jobs.extend(web_jobs)
                
                # Rate limiting to be respectful
                time.sleep(random.uniform(2, 5))
                
                if len(all_jobs) >= max_articles:
                    break
            
            # Remove duplicates and filter for quality
            unique_jobs = self.deduplicate_and_filter(all_jobs)
            
            self.logger.info(f"Found {len(unique_jobs)} unique job postings from newspapers")
            return unique_jobs[:max_articles]
            
        except Exception as e:
            self.logger.error(f"Error scraping newspapers: {e}")
            return []

    def scrape_rss_feeds(self, source_config: Dict) -> List[Dict]:
        """Scrape RSS feeds for job-related articles"""
        jobs = []
        
        try:
            for feed_url in source_config.get('rss_feeds', []):
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:20]:  # Limit to recent entries
                        job_data = self.extract_job_from_article(entry, source_config)
                        if job_data:
                            jobs.append(job_data)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    self.logger.warning(f"Error parsing RSS feed {feed_url}: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error scraping RSS feeds: {e}")
            return []

    def scrape_web_sections(self, source_config: Dict) -> List[Dict]:
        """Scrape web sections for job postings"""
        jobs = []
        
        try:
            for section_path in source_config.get('job_sections', []):
                try:
                    url = urljoin(source_config['base_url'], section_path)
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        section_jobs = self.extract_jobs_from_page(soup, source_config, url)
                        jobs.extend(section_jobs)
                    
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    self.logger.warning(f"Error scraping section {section_path}: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error scraping web sections: {e}")
            return []

    def extract_job_from_article(self, article, source_config: Dict) -> Optional[Dict]:
        """Extract job information from a news article"""
        try:
            title = article.get('title', '')
            summary = article.get('summary', '')
            content = f"{title} {summary}"
            
            # Check if article is job-related
            if not self.is_job_related(content):
                return None
            
            # Extract job details
            job_info = self.parse_job_details(content)
            
            if job_info:
                return {
                    'title': job_info.get('title', title),
                    'company': job_info.get('company', self.extract_company_from_text(content)),
                    'location': job_info.get('location', self.extract_location_from_text(content)),
                    'description': summary,
                    'source': source_config['name'],
                    'url': article.get('link', ''),
                    'posted_date': self.parse_date(article.get('published', '')),
                    'salary': job_info.get('salary', ''),
                    'job_type': job_info.get('job_type', 'full-time'),
                    'platform': 'newspaper',
                    'scraped_at': datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting job from article: {e}")
            return None

    def extract_jobs_from_page(self, soup: BeautifulSoup, source_config: Dict, url: str) -> List[Dict]:
        """Extract job postings from a web page"""
        jobs = []
        
        try:
            # Look for articles, headlines, and content blocks
            content_selectors = [
                'article', 'div.article', 'div.story', 'div.content',
                'h1', 'h2', 'h3', 'h4', 'p', 'div.headline'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                
                for element in elements[:50]:  # Limit processing
                    text_content = element.get_text(strip=True)
                    
                    if self.is_job_related(text_content) and len(text_content) > 50:
                        job_info = self.parse_job_details(text_content)
                        
                        if job_info:
                            # Try to find a more specific URL
                            link_element = element.find('a', href=True)
                            job_url = urljoin(url, link_element['href']) if link_element else url
                            
                            job_data = {
                                'title': job_info.get('title', text_content[:100]),
                                'company': job_info.get('company', self.extract_company_from_text(text_content)),
                                'location': job_info.get('location', self.extract_location_from_text(text_content)),
                                'description': text_content[:500],
                                'source': source_config['name'],
                                'url': job_url,
                                'posted_date': datetime.now().isoformat(),
                                'salary': job_info.get('salary', ''),
                                'job_type': job_info.get('job_type', 'full-time'),
                                'platform': 'newspaper',
                                'scraped_at': datetime.now().isoformat()
                            }
                            
                            jobs.append(job_data)
                            
                            if len(jobs) >= 10:  # Limit per page
                                break
                
                if len(jobs) >= 10:
                    break
            
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error extracting jobs from page: {e}")
            return []

    def is_job_related(self, text: str) -> bool:
        """Check if text content is related to job postings"""
        text_lower = text.lower()
        
        # Check for job keywords
        job_keyword_count = sum(1 for keyword in self.job_keywords if keyword in text_lower)
        
        # Check for company indicators
        company_indicator_count = sum(1 for indicator in self.company_indicators if indicator in text_lower)
        
        # Minimum threshold for job-related content
        return job_keyword_count >= 2 or (job_keyword_count >= 1 and company_indicator_count >= 1)

    def parse_job_details(self, text: str) -> Optional[Dict]:
        """Parse job details from text content"""
        try:
            details = {}
            
            # Extract job title (look for common patterns)
            title_patterns = [
                r'(?i)(?:hiring|seeking|looking for|position|job|role|opening)\s+(?:for\s+)?([^,.!?]+)',
                r'(?i)([^,.!?]+)\s+(?:position|job|role|opening|vacancy)',
                r'(?i)(software engineer|developer|programmer|analyst|manager|director|coordinator|specialist)',
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, text)
                if match:
                    details['title'] = match.group(1).strip()
                    break
            
            # Extract salary information
            salary_patterns = [
                r'(?i)\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|\-)\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'(?i)\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'(?i)(\d{1,3}k)\s*(?:to|\-)\s*(\d{1,3}k)',
            ]
            
            for pattern in salary_patterns:
                match = re.search(pattern, text)
                if match:
                    if len(match.groups()) == 2:
                        details['salary'] = f"${match.group(1)} - ${match.group(2)}"
                    else:
                        details['salary'] = f"${match.group(1)}"
                    break
            
            # Extract job type
            if re.search(r'(?i)remote|work from home|telecommute', text):
                details['job_type'] = 'remote'
            elif re.search(r'(?i)part.?time|contract|freelance|temporary', text):
                details['job_type'] = 'part-time'
            else:
                details['job_type'] = 'full-time'
            
            return details if details else None
            
        except Exception as e:
            self.logger.error(f"Error parsing job details: {e}")
            return None

    def extract_company_from_text(self, text: str) -> str:
        """Extract company name from text"""
        try:
            # Look for company patterns
            company_patterns = [
                r'(?i)(?:at|with|for|by)\s+([A-Z][a-zA-Z\s&]+(?:Inc|Corp|Corporation|Ltd|Limited|LLC))',
                r'(?i)([A-Z][a-zA-Z\s&]+(?:Inc|Corp|Corporation|Ltd|Limited|LLC))',
                r'(?i)([A-Z][a-zA-Z\s&]+(?:Company|Technologies|Solutions|Services))',
            ]
            
            for pattern in company_patterns:
                match = re.search(pattern, text)
                if match:
                    company = match.group(1).strip()
                    if len(company) > 2 and len(company) < 100:
                        return company
            
            return "Unknown Company"
            
        except Exception as e:
            self.logger.error(f"Error extracting company: {e}")
            return "Unknown Company"

    def extract_location_from_text(self, text: str) -> str:
        """Extract location from text"""
        try:
            # Canadian cities
            canadian_cities = [
                'Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Edmonton', 'Ottawa',
                'Winnipeg', 'Quebec City', 'Hamilton', 'Kitchener', 'London',
                'Victoria', 'Halifax', 'Oshawa', 'Windsor', 'Saskatoon', 'Regina'
            ]
            
            # US cities
            us_cities = [
                'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
                'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
                'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis',
                'Seattle', 'Denver', 'Washington', 'Boston', 'Nashville', 'Baltimore',
                'Portland', 'Las Vegas', 'Detroit', 'Memphis', 'Louisville', 'Milwaukee',
                'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Mesa', 'Kansas City',
                'Atlanta', 'Long Beach', 'Colorado Springs', 'Raleigh', 'Miami', 'Virginia Beach'
            ]
            
            all_cities = canadian_cities + us_cities
            
            for city in all_cities:
                if city.lower() in text.lower():
                    return city
            
            # Look for remote work indicators
            if re.search(r'(?i)remote|work from home|anywhere', text):
                return "Remote"
            
            return "Location not specified"
            
        except Exception as e:
            self.logger.error(f"Error extracting location: {e}")
            return "Location not specified"

    def parse_date(self, date_str: str) -> str:
        """Parse date string to ISO format"""
        try:
            if not date_str:
                return datetime.now().isoformat()
            
            # Try different date formats
            formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%d %b %Y',
                '%b %d, %Y'
            ]
            
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.isoformat()
                except ValueError:
                    continue
            
            return datetime.now().isoformat()
            
        except Exception as e:
            self.logger.error(f"Error parsing date: {e}")
            return datetime.now().isoformat()

    def deduplicate_and_filter(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicates and filter for quality"""
        try:
            seen_jobs = set()
            unique_jobs = []
            
            for job in jobs:
                # Create a unique identifier
                job_id = f"{job.get('title', '')}-{job.get('company', '')}-{job.get('location', '')}"
                job_id = job_id.lower().strip()
                
                if job_id not in seen_jobs and len(job.get('title', '')) > 5:
                    seen_jobs.add(job_id)
                    unique_jobs.append(job)
            
            return unique_jobs
            
        except Exception as e:
            self.logger.error(f"Error deduplicating jobs: {e}")
            return jobs

    def get_job_statistics(self, jobs: List[Dict]) -> Dict:
        """Get statistics about scraped jobs"""
        try:
            stats = {
                'total_jobs': len(jobs),
                'sources': {},
                'locations': {},
                'job_types': {},
                'companies': {}
            }
            
            for job in jobs:
                # Source stats
                source = job.get('source', 'Unknown')
                stats['sources'][source] = stats['sources'].get(source, 0) + 1
                
                # Location stats
                location = job.get('location', 'Unknown')
                stats['locations'][location] = stats['locations'].get(location, 0) + 1
                
                # Job type stats
                job_type = job.get('job_type', 'Unknown')
                stats['job_types'][job_type] = stats['job_types'].get(job_type, 0) + 1
                
                # Company stats
                company = job.get('company', 'Unknown')
                stats['companies'][company] = stats['companies'].get(company, 0) + 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error generating statistics: {e}")
            return {'total_jobs': len(jobs)} 