from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from typing import List, Dict, Optional
import random

class JobScraper:
    def __init__(self, headless: bool = True):
        self.setup_driver(headless)
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self, headless: bool):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
    def scrape_linkedin_jobs(self, keywords: str, location: str, max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from LinkedIn"""
        jobs = []
        try:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
            self.driver.get(search_url)
            time.sleep(random.uniform(2, 4))
            
            # Wait for job listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-job-id]"))
            )
            
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-job-id]")
            
            for i, job_element in enumerate(job_elements[:max_jobs]):
                try:
                    job_id = job_element.get_attribute("data-job-id")
                    
                    # Click on job to get details
                    job_element.click()
                    time.sleep(random.uniform(1, 2))
                    
                    # Extract job details
                    job_data = self.extract_linkedin_job_details(job_id)
                    if job_data:
                        jobs.append(job_data)
                        
                except Exception as e:
                    self.logger.error(f"Error extracting job {i}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error scraping LinkedIn: {e}")
            
        return jobs
    
    def extract_linkedin_job_details(self, job_id: str) -> Optional[Dict]:
        """Extract detailed job information from LinkedIn"""
        try:
            # Wait for job details to load
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".job-details"))
            )
            
            title_element = self.driver.find_element(By.CSS_SELECTOR, "h1.job-title")
            company_element = self.driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name")
            location_element = self.driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__bullet")
            description_element = self.driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-description")
            
            # Try to find apply button
            apply_button = None
            try:
                apply_button = self.driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button")
            except:
                pass
                
            return {
                "id": job_id,
                "title": title_element.text.strip(),
                "company": company_element.text.strip(),
                "location": location_element.text.strip(),
                "description": description_element.text.strip(),
                "platform": "linkedin",
                "apply_url": self.driver.current_url,
                "can_apply": apply_button is not None,
                "scraped_at": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting job details: {e}")
            return None
    
    def scrape_indeed_jobs(self, keywords: str, location: str, max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from Indeed"""
        jobs = []
        try:
            search_url = f"https://www.indeed.com/jobs?q={keywords}&l={location}"
            self.driver.get(search_url)
            time.sleep(random.uniform(2, 4))
            
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
            
            for i, job_element in enumerate(job_elements[:max_jobs]):
                try:
                    job_id = job_element.get_attribute("data-jk")
                    
                    # Extract job details
                    job_data = self.extract_indeed_job_details(job_element, job_id)
                    if job_data:
                        jobs.append(job_data)
                        
                except Exception as e:
                    self.logger.error(f"Error extracting Indeed job {i}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error scraping Indeed: {e}")
            
        return jobs
    
    def extract_indeed_job_details(self, job_element, job_id: str) -> Optional[Dict]:
        """Extract job details from Indeed job element"""
        try:
            title = job_element.find_element(By.CSS_SELECTOR, "h2.jobTitle a").text.strip()
            company = job_element.find_element(By.CSS_SELECTOR, ".companyName").text.strip()
            location = job_element.find_element(By.CSS_SELECTOR, ".companyLocation").text.strip()
            
            # Get job URL
            job_link = job_element.find_element(By.CSS_SELECTOR, "h2.jobTitle a").get_attribute("href")
            
            return {
                "id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "platform": "indeed",
                "apply_url": job_link,
                "can_apply": True,
                "scraped_at": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting Indeed job details: {e}")
            return None
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit() 