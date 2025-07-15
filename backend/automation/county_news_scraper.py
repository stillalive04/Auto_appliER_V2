import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

class CountyNewsJobScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = None
        self.discovered_jobs = []
        self.processed_urls = set()
        
        # US Counties database with major newspapers
        self.county_newspapers = self.load_county_newspapers()
        
        # Job-related keywords to identify job postings
        self.job_keywords = {
            'titles': [
                'hiring', 'job', 'position', 'career', 'employment', 'opportunity',
                'seeking', 'wanted', 'opening', 'vacancy', 'recruit', 'apply',
                'intern', 'internship', 'entry level', 'junior', 'senior', 'lead',
                'manager', 'director', 'executive', 'ceo', 'cto', 'cfo', 'vp'
            ],
            'sections': [
                'jobs', 'careers', 'employment', 'classifieds', 'help wanted',
                'opportunities', 'work', 'hiring', 'positions'
            ]
        }
        
        # Enhanced job types and experience levels
        self.job_types = [
            'Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship',
            'Freelance', 'Remote', 'Hybrid', 'On-site', 'Consultant',
            'W2', 'C2H', '1099', 'Corp-to-Corp', 'Outsource', 'Project-based'
        ]
        
        self.experience_levels = [
            'Internship', 'Entry Level', 'Junior', 'Mid Level', 'Senior',
            'Lead', 'Principal', 'Manager', 'Senior Manager', 'Director',
            'Senior Director', 'VP', 'Senior VP', 'Executive VP', 'C-Suite',
            'CEO', 'CTO', 'CFO', 'COO', 'CHRO', 'CMO', 'President', 'Founder'
        ]

    def load_county_newspapers(self) -> Dict[str, List[Dict]]:
        """Load comprehensive database of county newspapers across all US states"""
        return {
            # Major metropolitan areas
            'california': [
                {'name': 'Los Angeles Times', 'url': 'https://www.latimes.com', 'county': 'Los Angeles'},
                {'name': 'San Francisco Chronicle', 'url': 'https://www.sfchronicle.com', 'county': 'San Francisco'},
                {'name': 'San Diego Union-Tribune', 'url': 'https://www.sandiegouniontribune.com', 'county': 'San Diego'},
                {'name': 'Sacramento Bee', 'url': 'https://www.sacbee.com', 'county': 'Sacramento'},
                {'name': 'Orange County Register', 'url': 'https://www.ocregister.com', 'county': 'Orange'},
                {'name': 'Fresno Bee', 'url': 'https://www.fresnobee.com', 'county': 'Fresno'},
                {'name': 'Modesto Bee', 'url': 'https://www.modbee.com', 'county': 'Stanislaus'},
                {'name': 'Bakersfield Californian', 'url': 'https://www.bakersfield.com', 'county': 'Kern'},
                {'name': 'Stockton Record', 'url': 'https://www.recordnet.com', 'county': 'San Joaquin'},
                {'name': 'Riverside Press-Enterprise', 'url': 'https://www.pe.com', 'county': 'Riverside'},
                {'name': 'Ventura County Star', 'url': 'https://www.vcstar.com', 'county': 'Ventura'},
                {'name': 'Santa Barbara News-Press', 'url': 'https://newspress.com', 'county': 'Santa Barbara'},
                {'name': 'Monterey Herald', 'url': 'https://www.montereyherald.com', 'county': 'Monterey'},
                {'name': 'Santa Rosa Press Democrat', 'url': 'https://www.pressdemocrat.com', 'county': 'Sonoma'},
                {'name': 'Salinas Californian', 'url': 'https://www.thecalifornian.com', 'county': 'Monterey'},
            ],
            'texas': [
                {'name': 'Houston Chronicle', 'url': 'https://www.houstonchronicle.com', 'county': 'Harris'},
                {'name': 'Dallas Morning News', 'url': 'https://www.dallasnews.com', 'county': 'Dallas'},
                {'name': 'San Antonio Express-News', 'url': 'https://www.expressnews.com', 'county': 'Bexar'},
                {'name': 'Austin American-Statesman', 'url': 'https://www.statesman.com', 'county': 'Travis'},
                {'name': 'Fort Worth Star-Telegram', 'url': 'https://www.star-telegram.com', 'county': 'Tarrant'},
                {'name': 'El Paso Times', 'url': 'https://www.elpasotimes.com', 'county': 'El Paso'},
                {'name': 'Corpus Christi Caller-Times', 'url': 'https://www.caller.com', 'county': 'Nueces'},
                {'name': 'Lubbock Avalanche-Journal', 'url': 'https://www.lubbockonline.com', 'county': 'Lubbock'},
                {'name': 'Amarillo Globe-News', 'url': 'https://www.amarillo.com', 'county': 'Potter'},
                {'name': 'Beaumont Enterprise', 'url': 'https://www.beaumontenterprise.com', 'county': 'Jefferson'},
                {'name': 'Waco Tribune-Herald', 'url': 'https://www.wacotrib.com', 'county': 'McLennan'},
                {'name': 'Tyler Morning Telegraph', 'url': 'https://www.tylerpaper.com', 'county': 'Smith'},
                {'name': 'Longview News-Journal', 'url': 'https://www.news-journal.com', 'county': 'Gregg'},
                {'name': 'Abilene Reporter-News', 'url': 'https://www.reporternews.com', 'county': 'Taylor'},
                {'name': 'Midland Reporter-Telegram', 'url': 'https://www.mrt.com', 'county': 'Midland'},
            ],
            'florida': [
                {'name': 'Miami Herald', 'url': 'https://www.miamiherald.com', 'county': 'Miami-Dade'},
                {'name': 'Tampa Bay Times', 'url': 'https://www.tampabay.com', 'county': 'Pinellas'},
                {'name': 'Orlando Sentinel', 'url': 'https://www.orlandosentinel.com', 'county': 'Orange'},
                {'name': 'Sun Sentinel', 'url': 'https://www.sun-sentinel.com', 'county': 'Broward'},
                {'name': 'Jacksonville Times-Union', 'url': 'https://www.jacksonville.com', 'county': 'Duval'},
                {'name': 'Palm Beach Post', 'url': 'https://www.palmbeachpost.com', 'county': 'Palm Beach'},
                {'name': 'Tallahassee Democrat', 'url': 'https://www.tallahassee.com', 'county': 'Leon'},
                {'name': 'Pensacola News Journal', 'url': 'https://www.pnj.com', 'county': 'Escambia'},
                {'name': 'Gainesville Sun', 'url': 'https://www.gainesville.com', 'county': 'Alachua'},
                {'name': 'Sarasota Herald-Tribune', 'url': 'https://www.heraldtribune.com', 'county': 'Sarasota'},
                {'name': 'Naples Daily News', 'url': 'https://www.naplesnews.com', 'county': 'Collier'},
                {'name': 'Daytona Beach News-Journal', 'url': 'https://www.news-journalonline.com', 'county': 'Volusia'},
                {'name': 'Lakeland Ledger', 'url': 'https://www.theledger.com', 'county': 'Polk'},
                {'name': 'Florida Today', 'url': 'https://www.floridatoday.com', 'county': 'Brevard'},
                {'name': 'Ocala Star-Banner', 'url': 'https://www.ocala.com', 'county': 'Marion'},
            ],
            'new_york': [
                {'name': 'New York Times', 'url': 'https://www.nytimes.com', 'county': 'New York'},
                {'name': 'New York Post', 'url': 'https://nypost.com', 'county': 'New York'},
                {'name': 'Daily News', 'url': 'https://www.nydailynews.com', 'county': 'New York'},
                {'name': 'Buffalo News', 'url': 'https://buffalonews.com', 'county': 'Erie'},
                {'name': 'Rochester Democrat and Chronicle', 'url': 'https://www.democratandchronicle.com', 'county': 'Monroe'},
                {'name': 'Syracuse Post-Standard', 'url': 'https://www.syracuse.com', 'county': 'Onondaga'},
                {'name': 'Albany Times Union', 'url': 'https://www.timesunion.com', 'county': 'Albany'},
                {'name': 'Newsday', 'url': 'https://www.newsday.com', 'county': 'Nassau'},
                {'name': 'Staten Island Advance', 'url': 'https://www.silive.com', 'county': 'Richmond'},
                {'name': 'Journal News', 'url': 'https://www.lohud.com', 'county': 'Westchester'},
                {'name': 'Utica Observer-Dispatch', 'url': 'https://www.uticaod.com', 'county': 'Oneida'},
                {'name': 'Watertown Daily Times', 'url': 'https://www.watertowndailytimes.com', 'county': 'Jefferson'},
                {'name': 'Binghamton Press & Sun-Bulletin', 'url': 'https://www.pressconnects.com', 'county': 'Broome'},
                {'name': 'Elmira Star-Gazette', 'url': 'https://www.stargazette.com', 'county': 'Chemung'},
                {'name': 'Ithaca Journal', 'url': 'https://www.ithacajournal.com', 'county': 'Tompkins'},
            ],
            # Add more states and counties...
            'illinois': [
                {'name': 'Chicago Tribune', 'url': 'https://www.chicagotribune.com', 'county': 'Cook'},
                {'name': 'Chicago Sun-Times', 'url': 'https://chicago.suntimes.com', 'county': 'Cook'},
                {'name': 'Daily Herald', 'url': 'https://www.dailyherald.com', 'county': 'Cook'},
                {'name': 'Rockford Register Star', 'url': 'https://www.rrstar.com', 'county': 'Winnebago'},
                {'name': 'Peoria Journal Star', 'url': 'https://www.pjstar.com', 'county': 'Peoria'},
                {'name': 'State Journal-Register', 'url': 'https://www.sj-r.com', 'county': 'Sangamon'},
                {'name': 'Bloomington Pantagraph', 'url': 'https://www.pantagraph.com', 'county': 'McLean'},
                {'name': 'Quad-City Times', 'url': 'https://qctimes.com', 'county': 'Rock Island'},
                {'name': 'Herald & Review', 'url': 'https://herald-review.com', 'county': 'Macon'},
                {'name': 'Daily Chronicle', 'url': 'https://www.daily-chronicle.com', 'county': 'DeKalb'},
            ],
            # Continue with all 50 states...
            'ohio': [
                {'name': 'Cleveland Plain Dealer', 'url': 'https://www.cleveland.com', 'county': 'Cuyahoga'},
                {'name': 'Cincinnati Enquirer', 'url': 'https://www.cincinnati.com', 'county': 'Hamilton'},
                {'name': 'Columbus Dispatch', 'url': 'https://www.dispatch.com', 'county': 'Franklin'},
                {'name': 'Toledo Blade', 'url': 'https://www.toledoblade.com', 'county': 'Lucas'},
                {'name': 'Akron Beacon Journal', 'url': 'https://www.beaconjournal.com', 'county': 'Summit'},
                {'name': 'Dayton Daily News', 'url': 'https://www.daytondailynews.com', 'county': 'Montgomery'},
                {'name': 'Youngstown Vindicator', 'url': 'https://www.vindy.com', 'county': 'Mahoning'},
                {'name': 'Canton Repository', 'url': 'https://www.cantonrep.com', 'county': 'Stark'},
                {'name': 'Lima News', 'url': 'https://www.limaohio.com', 'county': 'Allen'},
                {'name': 'Mansfield News Journal', 'url': 'https://www.mansfieldnewsjournal.com', 'county': 'Richland'},
            ],
            # Add remaining states to reach 3,144+ counties
            'pennsylvania': [
                {'name': 'Philadelphia Inquirer', 'url': 'https://www.inquirer.com', 'county': 'Philadelphia'},
                {'name': 'Pittsburgh Post-Gazette', 'url': 'https://www.post-gazette.com', 'county': 'Allegheny'},
                {'name': 'Harrisburg Patriot-News', 'url': 'https://www.pennlive.com', 'county': 'Dauphin'},
                {'name': 'Allentown Morning Call', 'url': 'https://www.mcall.com', 'county': 'Lehigh'},
                {'name': 'Scranton Times-Tribune', 'url': 'https://www.thetimes-tribune.com', 'county': 'Lackawanna'},
                {'name': 'Erie Times-News', 'url': 'https://www.goerie.com', 'county': 'Erie'},
                {'name': 'York Daily Record', 'url': 'https://www.ydr.com', 'county': 'York'},
                {'name': 'Lancaster Intelligencer Journal', 'url': 'https://lancasteronline.com', 'county': 'Lancaster'},
                {'name': 'Reading Eagle', 'url': 'https://www.readingeagle.com', 'county': 'Berks'},
                {'name': 'Wilkes-Barre Times Leader', 'url': 'https://www.timesleader.com', 'county': 'Luzerne'},
            ],
            # Continue with remaining states to cover all 3,144+ counties...
        }

    async def initialize_session(self):
        """Initialize aiohttp session with proper headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
            connector=connector
        )

    async def scrape_all_counties(self, max_jobs_per_county: int = 50) -> List[Dict]:
        """Scrape job postings from all county newspapers"""
        if not self.session:
            await self.initialize_session()
        
        all_jobs = []
        county_count = 0
        
        for state, newspapers in self.county_newspapers.items():
            self.logger.info(f"Scraping {state.upper()} counties...")
            
            for newspaper in newspapers:
                county_count += 1
                try:
                    jobs = await self.scrape_newspaper_jobs(newspaper, max_jobs_per_county)
                    all_jobs.extend(jobs)
                    
                    self.logger.info(f"Found {len(jobs)} jobs from {newspaper['name']} ({newspaper['county']} County)")
                    
                    # Rate limiting
                    await asyncio.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    self.logger.error(f"Error scraping {newspaper['name']}: {e}")
                    continue
        
        self.logger.info(f"Completed scraping {county_count} counties, found {len(all_jobs)} total jobs")
        return all_jobs

    async def scrape_newspaper_jobs(self, newspaper: Dict, max_jobs: int) -> List[Dict]:
        """Scrape jobs from a specific newspaper"""
        jobs = []
        
        try:
            # First, try to find dedicated job/career sections
            job_urls = await self.find_job_sections(newspaper['url'])
            
            # If no dedicated sections, search main site
            if not job_urls:
                job_urls = [newspaper['url']]
            
            for url in job_urls[:5]:  # Limit to 5 sections per newspaper
                try:
                    page_jobs = await self.scrape_job_page(url, newspaper, max_jobs // len(job_urls))
                    jobs.extend(page_jobs)
                    
                    if len(jobs) >= max_jobs:
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error scraping job page {url}: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error scraping newspaper {newspaper['name']}: {e}")
        
        return jobs[:max_jobs]

    async def find_job_sections(self, base_url: str) -> List[str]:
        """Find job/career sections on newspaper websites"""
        job_urls = []
        
        try:
            async with self.session.get(base_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for job-related links
                    for link in soup.find_all('a', href=True):
                        href = link.get('href', '').lower()
                        text = link.get_text().lower()
                        
                        # Check if link is job-related
                        if any(keyword in href or keyword in text for keyword in self.job_keywords['sections']):
                            full_url = urljoin(base_url, link['href'])
                            if full_url not in job_urls:
                                job_urls.append(full_url)
                    
                    # Also check for classifieds sections
                    classifieds_patterns = [
                        r'classifieds?',
                        r'help.?wanted',
                        r'employment',
                        r'careers?',
                        r'jobs?'
                    ]
                    
                    for pattern in classifieds_patterns:
                        matches = soup.find_all('a', href=re.compile(pattern, re.I))
                        for match in matches:
                            full_url = urljoin(base_url, match['href'])
                            if full_url not in job_urls:
                                job_urls.append(full_url)
        
        except Exception as e:
            self.logger.error(f"Error finding job sections for {base_url}: {e}")
        
        return job_urls

    async def scrape_job_page(self, url: str, newspaper: Dict, max_jobs: int) -> List[Dict]:
        """Scrape individual job postings from a page"""
        jobs = []
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract job postings using multiple strategies
                    job_elements = self.find_job_elements(soup)
                    
                    for element in job_elements[:max_jobs]:
                        try:
                            job_data = await self.extract_job_data(element, newspaper, url)
                            if job_data and self.is_valid_job(job_data):
                                jobs.append(job_data)
                        except Exception as e:
                            self.logger.error(f"Error extracting job data: {e}")
                            continue
        
        except Exception as e:
            self.logger.error(f"Error scraping job page {url}: {e}")
        
        return jobs

    def find_job_elements(self, soup: BeautifulSoup) -> List:
        """Find job posting elements using various selectors"""
        job_elements = []
        
        # Common job posting selectors
        selectors = [
            '.job-listing', '.job-post', '.job-item', '.job-card',
            '.career-item', '.position-item', '.employment-item',
            '.classified-item', '.listing-item', '.ad-item',
            '[class*="job"]', '[class*="career"]', '[class*="position"]',
            '[class*="employment"]', '[class*="hiring"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            job_elements.extend(elements)
        
        # If no structured elements found, look for text patterns
        if not job_elements:
            # Look for paragraphs or divs containing job keywords
            all_elements = soup.find_all(['p', 'div', 'article', 'section'])
            for element in all_elements:
                text = element.get_text().lower()
                if any(keyword in text for keyword in self.job_keywords['titles']):
                    job_elements.append(element)
        
        return job_elements

    async def extract_job_data(self, element, newspaper: Dict, source_url: str) -> Dict:
        """Extract structured job data from HTML element"""
        job_data = {
            'id': f"{newspaper['county']}_{int(time.time())}_{random.randint(1000, 9999)}",
            'source': 'county_newspaper',
            'newspaper': newspaper['name'],
            'county': newspaper['county'],
            'state': newspaper.get('state', 'Unknown'),
            'source_url': source_url,
            'scraped_at': datetime.now().isoformat(),
            'platform': 'newspaper'
        }
        
        # Extract job title
        job_data['title'] = self.extract_job_title(element)
        
        # Extract company name
        job_data['company'] = self.extract_company_name(element)
        
        # Extract job description
        job_data['description'] = self.extract_job_description(element)
        
        # Extract location
        job_data['location'] = self.extract_location(element, newspaper)
        
        # Extract job type and experience level
        job_data['job_type'] = self.extract_job_type(element)
        job_data['experience_level'] = self.extract_experience_level(element)
        
        # Extract salary information
        job_data['salary'] = self.extract_salary(element)
        
        # Extract contact information
        job_data['contact'] = self.extract_contact_info(element)
        
        # Extract application instructions
        job_data['apply_instructions'] = self.extract_apply_instructions(element)
        
        # Generate apply URL if available
        job_data['apply_url'] = self.extract_apply_url(element, source_url)
        
        return job_data

    def extract_job_title(self, element) -> str:
        """Extract job title from element"""
        # Look for title in various places
        title_selectors = [
            'h1', 'h2', 'h3', 'h4', '.title', '.job-title', 
            '.position-title', '.role-title', '[class*="title"]'
        ]
        
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                if len(title) > 5 and len(title) < 200:  # Reasonable title length
                    return title
        
        # Fallback: look for text patterns
        text = element.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines[:5]:  # Check first 5 lines
            if any(keyword in line.lower() for keyword in ['hiring', 'seeking', 'wanted', 'position']):
                return line[:100]  # Truncate if too long
        
        return lines[0][:100] if lines else "Job Opening"

    def extract_company_name(self, element) -> str:
        """Extract real company name from element"""
        # Look for company name in various places
        company_selectors = [
            '.company', '.company-name', '.employer', '.business',
            '[class*="company"]', '[class*="employer"]', '[class*="business"]'
        ]
        
        for selector in company_selectors:
            company_elem = element.select_one(selector)
            if company_elem:
                company = company_elem.get_text().strip()
                if len(company) > 2 and len(company) < 100:
                    return company
        
        # Look for patterns like "Company: XYZ" or "Employer: ABC"
        text = element.get_text()
        patterns = [
            r'(?:company|employer|business):\s*([^\n\r]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|seeks|hiring)',
            r'(?:at|with)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) > 2 and len(company) < 100:
                    return company
        
        return "Local Business"

    def extract_job_description(self, element) -> str:
        """Extract job description"""
        # Remove unwanted elements
        for unwanted in element.find_all(['script', 'style', 'nav', 'header', 'footer']):
            unwanted.decompose()
        
        description = element.get_text().strip()
        
        # Clean up the description
        description = re.sub(r'\s+', ' ', description)  # Normalize whitespace
        description = description[:2000]  # Limit length
        
        return description

    def extract_location(self, element, newspaper: Dict) -> str:
        """Extract job location"""
        location_patterns = [
            r'(?:location|address):\s*([^\n\r]+)',
            r'(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})',
            r'([A-Z][a-z]+,\s*[A-Z]{2})',
        ]
        
        text = element.get_text()
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Default to newspaper's county
        return f"{newspaper['county']} County, {newspaper.get('state', 'US')}"

    def extract_job_type(self, element) -> str:
        """Extract job type from text"""
        text = element.get_text().lower()
        
        for job_type in self.job_types:
            if job_type.lower() in text:
                return job_type
        
        # Default patterns
        if any(word in text for word in ['full', 'permanent', 'regular']):
            return 'Full-time'
        elif any(word in text for word in ['part', 'partial']):
            return 'Part-time'
        elif any(word in text for word in ['contract', 'temporary', 'temp']):
            return 'Contract'
        elif any(word in text for word in ['intern', 'internship']):
            return 'Internship'
        elif any(word in text for word in ['remote', 'work from home']):
            return 'Remote'
        
        return 'Full-time'

    def extract_experience_level(self, element) -> str:
        """Extract experience level from text"""
        text = element.get_text().lower()
        
        # Check for specific experience levels
        for level in self.experience_levels:
            if level.lower() in text:
                return level
        
        # Pattern matching
        if any(word in text for word in ['intern', 'internship']):
            return 'Internship'
        elif any(word in text for word in ['entry', 'junior', 'new grad']):
            return 'Entry Level'
        elif any(word in text for word in ['senior', 'sr.', 'lead']):
            return 'Senior'
        elif any(word in text for word in ['manager', 'mgr']):
            return 'Manager'
        elif any(word in text for word in ['director', 'dir']):
            return 'Director'
        elif any(word in text for word in ['vp', 'vice president']):
            return 'VP'
        elif any(word in text for word in ['ceo', 'cto', 'cfo', 'coo']):
            return 'C-Suite'
        
        return 'Mid Level'

    def extract_salary(self, element) -> Optional[str]:
        """Extract salary information"""
        text = element.get_text()
        
        # Salary patterns
        salary_patterns = [
            r'\$[\d,]+(?:\.\d{2})?(?:\s*-\s*\$[\d,]+(?:\.\d{2})?)?(?:\s*(?:per|/)\s*(?:hour|hr|year|annually|month))?',
            r'(?:salary|pay|wage|compensation):\s*\$[\d,]+(?:\.\d{2})?(?:\s*-\s*\$[\d,]+(?:\.\d{2})?)?',
            r'[\d,]+(?:\.\d{2})?\s*(?:per|/)\s*(?:hour|hr|year|annually|month)',
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        return None

    def extract_contact_info(self, element) -> Dict:
        """Extract contact information"""
        text = element.get_text()
        contact = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone pattern
        phone_pattern = r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        return contact

    def extract_apply_instructions(self, element) -> str:
        """Extract application instructions"""
        text = element.get_text()
        
        # Look for application instructions
        instruction_patterns = [
            r'(?:apply|contact|send|email|call).*?(?:\.|$)',
            r'(?:to apply|application|interested).*?(?:\.|$)',
            r'(?:resume|cv).*?(?:\.|$)',
        ]
        
        for pattern in instruction_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                instruction = match.group(0).strip()
                if len(instruction) > 10:
                    return instruction[:500]  # Limit length
        
        return "Contact employer for application details"

    def extract_apply_url(self, element, source_url: str) -> Optional[str]:
        """Extract application URL if available"""
        # Look for application links
        apply_links = element.find_all('a', href=True)
        
        for link in apply_links:
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            if any(keyword in href or keyword in text for keyword in ['apply', 'application', 'job']):
                return urljoin(source_url, link['href'])
        
        return None

    def is_valid_job(self, job_data: Dict) -> bool:
        """Validate if extracted data represents a real job posting"""
        # Must have basic required fields
        if not job_data.get('title') or not job_data.get('company'):
            return False
        
        # Title should contain job-related keywords
        title_lower = job_data['title'].lower()
        if not any(keyword in title_lower for keyword in self.job_keywords['titles']):
            return False
        
        # Description should be substantial
        description = job_data.get('description', '')
        if len(description) < 50:
            return False
        
        # Avoid duplicate jobs
        job_signature = f"{job_data['title']}_{job_data['company']}_{job_data['county']}"
        if job_signature in self.processed_urls:
            return False
        
        self.processed_urls.add(job_signature)
        return True

    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()

    def get_total_counties_covered(self) -> int:
        """Get total number of counties covered"""
        total = 0
        for state, newspapers in self.county_newspapers.items():
            total += len(newspapers)
        return total

    async def scrape_jobs_by_state(self, state: str, max_jobs: int = 100) -> List[Dict]:
        """Scrape jobs from specific state"""
        if state.lower() not in self.county_newspapers:
            return []
        
        if not self.session:
            await self.initialize_session()
        
        newspapers = self.county_newspapers[state.lower()]
        all_jobs = []
        
        for newspaper in newspapers:
            try:
                jobs = await self.scrape_newspaper_jobs(newspaper, max_jobs // len(newspapers))
                all_jobs.extend(jobs)
                
                if len(all_jobs) >= max_jobs:
                    break
                    
            except Exception as e:
                self.logger.error(f"Error scraping {newspaper['name']}: {e}")
                continue
        
        return all_jobs[:max_jobs]

# Example usage
async def main():
    scraper = CountyNewsJobScraper()
    
    try:
        # Get total counties covered
        total_counties = scraper.get_total_counties_covered()
        print(f"Covering {total_counties} counties across the US")
        
        # Scrape jobs from specific state
        california_jobs = await scraper.scrape_jobs_by_state('california', max_jobs=50)
        print(f"Found {len(california_jobs)} jobs in California")
        
        # Scrape jobs from all counties (limited sample)
        # all_jobs = await scraper.scrape_all_counties(max_jobs_per_county=10)
        # print(f"Found {len(all_jobs)} total jobs across all counties")
        
    finally:
        await scraper.close_session()

if __name__ == "__main__":
    asyncio.run(main()) 