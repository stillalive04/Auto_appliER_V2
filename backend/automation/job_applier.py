from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import logging
from typing import Dict, List, Optional
import random

class JobApplier:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        
    async def apply_to_linkedin_job(self, job_data: Dict, user_profile: Dict) -> Dict:
        """Apply to a LinkedIn job automatically"""
        try:
            # Navigate to job URL
            self.driver.get(job_data["apply_url"])
            time.sleep(random.uniform(2, 4))
            
            # Find and click apply button
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-apply-button"))
            )
            apply_button.click()
            time.sleep(random.uniform(1, 3))
            
            # Handle LinkedIn Easy Apply flow
            return await self.handle_linkedin_easy_apply(job_data, user_profile)
            
        except Exception as e:
            self.logger.error(f"Error applying to LinkedIn job {job_data['id']}: {e}")
            return {
                "success": False,
                "error": str(e),
                "job_id": job_data["id"]
            }
    
    async def handle_linkedin_easy_apply(self, job_data: Dict, user_profile: Dict) -> Dict:
        """Handle LinkedIn Easy Apply process"""
        try:
            max_steps = 10
            current_step = 0
            
            while current_step < max_steps:
                try:
                    # Check if we're on the final submit page
                    if self.driver.find_elements(By.CSS_SELECTOR, "[data-easy-apply-next-button]"):
                        # Fill out form fields
                        await self.fill_application_form(user_profile)
                        
                        # Check for and solve CAPTCHA
                        captcha_solved = await self.solve_captcha_if_present()
                        
                        # Click next/submit button
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "[data-easy-apply-next-button]")
                        next_button.click()
                        time.sleep(random.uniform(1, 2))
                        
                    elif self.driver.find_elements(By.CSS_SELECTOR, "[data-easy-apply-submit-button]"):
                        # Final submit
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, "[data-easy-apply-submit-button]")
                        submit_button.click()
                        time.sleep(random.uniform(2, 4))
                        
                        # Check for success message
                        if self.driver.find_elements(By.CSS_SELECTOR, ".artdeco-inline-feedback--success"):
                            return {
                                "success": True,
                                "job_id": job_data["id"],
                                "platform": "linkedin",
                                "applied_at": time.time()
                            }
                        break
                        
                    else:
                        # No more buttons found, might be done
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error in Easy Apply step {current_step}: {e}")
                    break
                    
                current_step += 1
                
            return {
                "success": False,
                "error": "Easy Apply process incomplete",
                "job_id": job_data["id"]
            }
            
        except Exception as e:
            self.logger.error(f"Error in LinkedIn Easy Apply: {e}")
            return {
                "success": False,
                "error": str(e),
                "job_id": job_data["id"]
            }
    
    async def fill_application_form(self, user_profile: Dict):
        """Fill out application form fields automatically"""
        try:
            # Fill text inputs with comprehensive profile data
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            for input_field in text_inputs:
                field_name = input_field.get_attribute("name") or input_field.get_attribute("id")
                placeholder = input_field.get_attribute("placeholder") or ""
                
                if field_name and any(keyword in field_name.lower() for keyword in ["phone", "mobile"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("phone", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["website", "portfolio"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("portfolio_website", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["address", "street"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("address", ""))
                    
                elif field_name and "city" in field_name.lower():
                    input_field.clear()
                    input_field.send_keys(user_profile.get("city", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["state", "province"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("state", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["zip", "postal"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("zip_code", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["linkedin", "linkedinurl"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("linkedin_url", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["github", "githuburl"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("github_url", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["salary", "compensation"]):
                    salary_min = user_profile.get("salary_expectation_min", 0)
                    salary_max = user_profile.get("salary_expectation_max", 0)
                    if salary_min > 0:
                        input_field.clear()
                        input_field.send_keys(str(salary_min))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["university", "school", "college"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("university", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["major", "degree"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("major", ""))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["gpa"]):
                    gpa = user_profile.get("gpa", 0.0)
                    if gpa > 0:
                        input_field.clear()
                        input_field.send_keys(str(gpa))
                        
                elif field_name and any(keyword in field_name.lower() for keyword in ["start", "available", "availability"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("availability_date", "Immediately"))
                    
                elif field_name and any(keyword in field_name.lower() for keyword in ["notice", "period"]):
                    input_field.clear()
                    input_field.send_keys(user_profile.get("notice_period", "2 weeks"))
            
            # Handle dropdowns with comprehensive options
            dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "select")
            for dropdown in dropdowns:
                self.handle_dropdown_field(dropdown, user_profile)
                
            # Handle checkboxes (authorization to work, sponsorship, etc.)
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            for checkbox in checkboxes:
                label_text = self.get_checkbox_label(checkbox)
                if label_text:
                    label_lower = label_text.lower()
                    
                    # Work authorization checkbox
                    if any(keyword in label_lower for keyword in ["authorize", "authorized", "eligible to work"]):
                        work_auth = user_profile.get("work_authorization", "US Citizen")
                        if work_auth in ["US Citizen", "Green Card", "Permanent Resident"]:
                            if not checkbox.is_selected():
                                checkbox.click()
                    
                    # Visa sponsorship checkbox
                    elif any(keyword in label_lower for keyword in ["sponsorship", "visa sponsor", "require sponsor"]):
                        requires_sponsorship = user_profile.get("visa_sponsorship_required", False)
                        if requires_sponsorship and not checkbox.is_selected():
                            checkbox.click()
                        elif not requires_sponsorship and checkbox.is_selected():
                            checkbox.click()
                    
                    # Veteran status checkbox
                    elif any(keyword in label_lower for keyword in ["veteran", "military"]):
                        veteran_status = user_profile.get("veteran_status", "prefer_not_to_say")
                        if veteran_status == "veteran" and not checkbox.is_selected():
                            checkbox.click()
                    
                    # Disability status checkbox
                    elif any(keyword in label_lower for keyword in ["disability", "disabled"]):
                        disability_status = user_profile.get("disability_status", "prefer_not_to_say")
                        if disability_status == "yes" and not checkbox.is_selected():
                            checkbox.click()
                    
                    # Remote work checkbox
                    elif any(keyword in label_lower for keyword in ["remote", "work from home"]):
                        remote_pref = user_profile.get("remote_work_preference", "hybrid")
                        if remote_pref in ["remote", "hybrid"] and not checkbox.is_selected():
                            checkbox.click()
                    
                    # Relocation checkbox
                    elif any(keyword in label_lower for keyword in ["relocate", "relocation"]):
                        willing_relocate = user_profile.get("willing_to_relocate", False)
                        if willing_relocate and not checkbox.is_selected():
                            checkbox.click()
                        elif not willing_relocate and checkbox.is_selected():
                            checkbox.click()
                        
        except Exception as e:
            self.logger.error(f"Error filling application form: {e}")
    
    async def solve_captcha_if_present(self) -> bool:
        """Check for and solve CAPTCHA if present"""
        try:
            from automation.captcha_solver import CaptchaSolver
            captcha_solver = CaptchaSolver(self.driver)
            success = await captcha_solver.solve_captcha()
            
            if success:
                self.logger.info("CAPTCHA solved successfully")
            else:
                self.logger.warning("CAPTCHA solving failed or no CAPTCHA found")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error solving CAPTCHA: {e}")
            return False
    
    def handle_dropdown_field(self, dropdown, user_profile: Dict):
        """Handle dropdown field selection with comprehensive options"""
        try:
            select = Select(dropdown)
            
            # Get field context
            field_name = dropdown.get_attribute("name") or dropdown.get_attribute("id") or ""
            field_lower = field_name.lower()
            
            # Experience level dropdown
            if any(keyword in field_lower for keyword in ["experience", "level", "seniority"]):
                experience_years = user_profile.get("experience_years", 0)
                if experience_years >= 5:
                    self.select_option_by_text(select, ["5+", "Senior", "5-10", "Expert", "Lead"])
                elif experience_years >= 2:
                    self.select_option_by_text(select, ["2-5", "Mid", "3-5", "Intermediate", "Mid-level"])
                else:
                    self.select_option_by_text(select, ["1-2", "Entry", "Junior", "0-2", "Entry-level"])
            
            # Education level dropdown
            elif any(keyword in field_lower for keyword in ["education", "degree", "qualification"]):
                education_level = user_profile.get("education_level", "bachelor")
                if education_level == "phd":
                    self.select_option_by_text(select, ["PhD", "Doctorate", "Ph.D"])
                elif education_level == "master":
                    self.select_option_by_text(select, ["Master", "Masters", "MS", "MBA", "M.S."])
                elif education_level == "bachelor":
                    self.select_option_by_text(select, ["Bachelor", "Bachelors", "BS", "BA", "B.S.", "B.A."])
                elif education_level == "associate":
                    self.select_option_by_text(select, ["Associate", "Associates", "AS", "AA"])
                else:
                    self.select_option_by_text(select, ["High School", "Secondary", "Diploma"])
            
            # Work authorization dropdown
            elif any(keyword in field_lower for keyword in ["authorization", "work auth", "status", "visa"]):
                work_auth = user_profile.get("work_authorization", "US Citizen")
                if work_auth == "US Citizen":
                    self.select_option_by_text(select, ["US Citizen", "Citizen", "U.S. Citizen"])
                elif work_auth == "Green Card":
                    self.select_option_by_text(select, ["Green Card", "Permanent Resident", "LPR"])
                elif work_auth == "H1B":
                    self.select_option_by_text(select, ["H1B", "H-1B", "H1-B"])
                elif work_auth == "F1 OPT":
                    self.select_option_by_text(select, ["F1 OPT", "F-1 OPT", "OPT"])
                elif work_auth == "L1":
                    self.select_option_by_text(select, ["L1", "L-1"])
                else:
                    self.select_option_by_text(select, ["Other", "Require Sponsorship"])
            
            # Gender dropdown
            elif any(keyword in field_lower for keyword in ["gender", "sex"]):
                gender = user_profile.get("gender", "prefer_not_to_say")
                if gender == "male":
                    self.select_option_by_text(select, ["Male", "M"])
                elif gender == "female":
                    self.select_option_by_text(select, ["Female", "F"])
                elif gender == "non_binary":
                    self.select_option_by_text(select, ["Non-binary", "Other", "Non binary"])
                else:
                    self.select_option_by_text(select, ["Prefer not to say", "Decline to answer", "Not specified"])
            
            # Veteran status dropdown
            elif any(keyword in field_lower for keyword in ["veteran", "military"]):
                veteran_status = user_profile.get("veteran_status", "prefer_not_to_say")
                if veteran_status == "veteran":
                    self.select_option_by_text(select, ["Yes", "Veteran", "Protected Veteran"])
                elif veteran_status == "not_veteran":
                    self.select_option_by_text(select, ["No", "Not a veteran", "Not veteran"])
                else:
                    self.select_option_by_text(select, ["Prefer not to say", "Decline to answer"])
            
            # Disability status dropdown
            elif any(keyword in field_lower for keyword in ["disability", "disabled"]):
                disability_status = user_profile.get("disability_status", "prefer_not_to_say")
                if disability_status == "yes":
                    self.select_option_by_text(select, ["Yes", "I have a disability"])
                elif disability_status == "no":
                    self.select_option_by_text(select, ["No", "I do not have a disability"])
                else:
                    self.select_option_by_text(select, ["Prefer not to say", "Decline to answer"])
            
            # Race/Ethnicity dropdown
            elif any(keyword in field_lower for keyword in ["race", "ethnicity", "ethnic"]):
                race = user_profile.get("race", "prefer_not_to_say")
                ethnicity = user_profile.get("ethnicity", "prefer_not_to_say")
                if race != "prefer_not_to_say":
                    self.select_option_by_text(select, [race, ethnicity])
                else:
                    self.select_option_by_text(select, ["Prefer not to say", "Decline to answer"])
            
            # Remote work preference dropdown
            elif any(keyword in field_lower for keyword in ["remote", "work location", "location preference"]):
                remote_pref = user_profile.get("remote_work_preference", "hybrid")
                if remote_pref == "remote":
                    self.select_option_by_text(select, ["Remote", "Fully Remote", "100% Remote"])
                elif remote_pref == "hybrid":
                    self.select_option_by_text(select, ["Hybrid", "Flexible", "Remote/Hybrid"])
                else:
                    self.select_option_by_text(select, ["On-site", "Office", "In-person"])
            
            # Salary type dropdown
            elif any(keyword in field_lower for keyword in ["salary type", "compensation", "pay type"]):
                salary_type = user_profile.get("salary_type", "annual")
                if salary_type == "hourly":
                    self.select_option_by_text(select, ["Hourly", "Per Hour", "Hour"])
                else:
                    self.select_option_by_text(select, ["Annual", "Yearly", "Per Year", "Salary"])
                    
        except Exception as e:
            self.logger.error(f"Error handling dropdown: {e}")
    
    def select_option_by_text(self, select, text_options: List[str]):
        """Select dropdown option by matching text"""
        try:
            options = select.options
            for option in options:
                for text in text_options:
                    if text.lower() in option.text.lower():
                        select.select_by_visible_text(option.text)
                        return
        except Exception as e:
            self.logger.error(f"Error selecting option: {e}")
    
    def get_checkbox_label(self, checkbox) -> str:
        """Get label text for checkbox"""
        try:
            # Try to find associated label
            label_id = checkbox.get_attribute("id")
            if label_id:
                label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{label_id}']")
                return label.text
                
            # Try parent element
            parent = checkbox.find_element(By.XPATH, "..")
            return parent.text
            
        except:
            return ""
    
    async def apply_to_indeed_job(self, job_data: Dict, user_profile: Dict) -> Dict:
        """Apply to Indeed job automatically"""
        try:
            # Navigate to job URL
            self.driver.get(job_data["apply_url"])
            time.sleep(random.uniform(2, 4))
            
            # Look for apply button
            apply_button = None
            apply_selectors = [
                ".jobsearch-IndeedApplyButton",
                ".jobsearch-SerpJobCard-footer button",
                "[data-tn-element='applyButton']"
            ]
            
            for selector in apply_selectors:
                try:
                    apply_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
                    
            if not apply_button:
                return {
                    "success": False,
                    "error": "No apply button found",
                    "job_id": job_data["id"]
                }
            
            apply_button.click()
            time.sleep(random.uniform(2, 4))
            
            # Handle Indeed application process
            return await self.handle_indeed_application(job_data, user_profile)
            
        except Exception as e:
            self.logger.error(f"Error applying to Indeed job {job_data['id']}: {e}")
            return {
                "success": False,
                "error": str(e),
                "job_id": job_data["id"]
            }
    
    async def handle_indeed_application(self, job_data: Dict, user_profile: Dict) -> Dict:
        """Handle Indeed application process"""
        try:
            # Fill out Indeed application form
            await self.fill_indeed_form(user_profile)
            
            # Submit application
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            time.sleep(random.uniform(2, 4))
            
            # Check for success indicators
            success_indicators = [
                ".jobsearch-ApplicationComplete",
                ".ia-ApplicationConfirmation",
                "[data-testid='application-complete']"
            ]
            
            for indicator in success_indicators:
                if self.driver.find_elements(By.CSS_SELECTOR, indicator):
                    return {
                        "success": True,
                        "job_id": job_data["id"],
                        "platform": "indeed",
                        "applied_at": time.time()
                    }
            
            return {
                "success": False,
                "error": "Application status unclear",
                "job_id": job_data["id"]
            }
            
        except Exception as e:
            self.logger.error(f"Error in Indeed application: {e}")
            return {
                "success": False,
                "error": str(e),
                "job_id": job_data["id"]
            }
    
    async def fill_indeed_form(self, user_profile: Dict):
        """Fill Indeed application form with comprehensive profile data"""
        try:
            # Fill basic info
            name_field = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='name']")
            if name_field:
                name_field[0].clear()
                name_field[0].send_keys(user_profile.get("full_name", ""))
                
            email_field = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
            if email_field:
                email_field[0].clear()
                email_field[0].send_keys(user_profile.get("email", ""))
                
            phone_field = self.driver.find_elements(By.CSS_SELECTOR, "input[type='tel']")
            if phone_field:
                phone_field[0].clear()
                phone_field[0].send_keys(user_profile.get("phone", ""))
            
            # Fill address fields
            address_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='address']")
            if address_fields:
                address_fields[0].clear()
                address_fields[0].send_keys(user_profile.get("address", ""))
            
            city_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='city']")
            if city_fields:
                city_fields[0].clear()
                city_fields[0].send_keys(user_profile.get("city", ""))
            
            state_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='state']")
            if state_fields:
                state_fields[0].clear()
                state_fields[0].send_keys(user_profile.get("state", ""))
            
            zip_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='zip']")
            if zip_fields:
                zip_fields[0].clear()
                zip_fields[0].send_keys(user_profile.get("zip_code", ""))
            
            # Fill professional links
            linkedin_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='linkedin']")
            if linkedin_fields:
                linkedin_fields[0].clear()
                linkedin_fields[0].send_keys(user_profile.get("linkedin_url", ""))
            
            # Handle dropdowns and checkboxes using the comprehensive form filling logic
            await self.fill_application_form(user_profile)
                
        except Exception as e:
            self.logger.error(f"Error filling Indeed form: {e}") 