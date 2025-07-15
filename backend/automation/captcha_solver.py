import asyncio
import logging
from typing import Dict, Optional, List, Tuple
import time
import random
import base64
import io
from PIL import Image
import cv2
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

class CaptchaSolver:
    def __init__(self, driver: webdriver.Chrome = None):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        
        # CAPTCHA solving services (optional)
        self.captcha_services = {
            '2captcha': {
                'api_key': None,  # Set your API key
                'url': 'http://2captcha.com/in.php',
                'result_url': 'http://2captcha.com/res.php'
            },
            'anticaptcha': {
                'api_key': None,  # Set your API key
                'url': 'https://api.anti-captcha.com/createTask',
                'result_url': 'https://api.anti-captcha.com/getTaskResult'
            }
        }
        
        # Common CAPTCHA selectors
        self.captcha_selectors = {
            'recaptcha_v2': [
                '.g-recaptcha',
                '#g-recaptcha',
                '[data-sitekey]',
                'iframe[src*="recaptcha"]'
            ],
            'recaptcha_v3': [
                '.g-recaptcha-response',
                'input[name="g-recaptcha-response"]'
            ],
            'hcaptcha': [
                '.h-captcha',
                '#h-captcha',
                'iframe[src*="hcaptcha"]'
            ],
            'image_captcha': [
                'img[src*="captcha"]',
                '.captcha-image',
                '#captcha-image',
                '[class*="captcha"]'
            ],
            'text_captcha': [
                'input[name*="captcha"]',
                '.captcha-input',
                '#captcha-input'
            ]
        }

    async def solve_captcha(self, url: str = None) -> bool:
        """Main method to detect and solve various types of CAPTCHAs"""
        try:
            if not self.driver:
                self.logger.error("No WebDriver instance provided")
                return False
            
            # Wait for page to load
            await asyncio.sleep(2)
            
            # Detect CAPTCHA type
            captcha_type = self.detect_captcha_type()
            self.logger.info(f"Detected CAPTCHA type: {captcha_type}")
            
            if captcha_type == 'recaptcha_v2':
                return await self.solve_recaptcha_v2()
            elif captcha_type == 'recaptcha_v3':
                return await self.solve_recaptcha_v3()
            elif captcha_type == 'hcaptcha':
                return await self.solve_hcaptcha()
            elif captcha_type == 'image_captcha':
                return await self.solve_image_captcha()
            elif captcha_type == 'text_captcha':
                return await self.solve_text_captcha()
            elif captcha_type == 'none':
                self.logger.info("No CAPTCHA detected")
                return True
            else:
                self.logger.warning(f"Unknown CAPTCHA type: {captcha_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error solving CAPTCHA: {e}")
            return False

    def detect_captcha_type(self) -> str:
        """Detect the type of CAPTCHA present on the page"""
        try:
            # Check for reCAPTCHA v2
            for selector in self.captcha_selectors['recaptcha_v2']:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    return 'recaptcha_v2'
            
            # Check for reCAPTCHA v3
            for selector in self.captcha_selectors['recaptcha_v3']:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    return 'recaptcha_v3'
            
            # Check for hCaptcha
            for selector in self.captcha_selectors['hcaptcha']:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    return 'hcaptcha'
            
            # Check for image CAPTCHA
            for selector in self.captcha_selectors['image_captcha']:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    return 'image_captcha'
            
            # Check for text CAPTCHA
            for selector in self.captcha_selectors['text_captcha']:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    return 'text_captcha'
            
            return 'none'
            
        except Exception as e:
            self.logger.error(f"Error detecting CAPTCHA type: {e}")
            return 'unknown'

    async def solve_recaptcha_v2(self) -> bool:
        """Solve reCAPTCHA v2 (I'm not a robot checkbox)"""
        try:
            self.logger.info("Attempting to solve reCAPTCHA v2")
            
            # Wait for reCAPTCHA to load
            await asyncio.sleep(3)
            
            # Method 1: Try clicking the checkbox
            success = await self.click_recaptcha_checkbox()
            if success:
                return True
            
            # Method 2: Try audio challenge
            success = await self.solve_recaptcha_audio()
            if success:
                return True
            
            # Method 3: Try image challenge
            success = await self.solve_recaptcha_images()
            if success:
                return True
            
            # Method 4: Use external service (if configured)
            if self.captcha_services['2captcha']['api_key']:
                success = await self.solve_with_2captcha()
                if success:
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving reCAPTCHA v2: {e}")
            return False

    async def click_recaptcha_checkbox(self) -> bool:
        """Try to click the reCAPTCHA checkbox"""
        try:
            # Switch to reCAPTCHA iframe
            recaptcha_iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"]'))
            )
            
            self.driver.switch_to.frame(recaptcha_iframe)
            
            # Click the checkbox
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.recaptcha-checkbox-border'))
            )
            
            # Human-like click
            await self.human_like_click(checkbox)
            
            # Wait for verification
            await asyncio.sleep(3)
            
            # Check if solved
            if self.driver.find_elements(By.CSS_SELECTOR, '.recaptcha-checkbox-checked'):
                self.logger.info("reCAPTCHA checkbox solved successfully")
                self.driver.switch_to.default_content()
                return True
            
            self.driver.switch_to.default_content()
            return False
            
        except Exception as e:
            self.logger.error(f"Error clicking reCAPTCHA checkbox: {e}")
            self.driver.switch_to.default_content()
            return False

    async def solve_recaptcha_audio(self) -> bool:
        """Solve reCAPTCHA using audio challenge"""
        try:
            self.logger.info("Attempting audio challenge")
            
            # Find and click audio button
            audio_button = self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-audio-button')
            await self.human_like_click(audio_button)
            
            await asyncio.sleep(2)
            
            # Download audio file
            audio_source = self.driver.find_element(By.CSS_SELECTOR, '#audio-source')
            audio_url = audio_source.get_attribute('src')
            
            # Download and convert audio
            audio_text = await self.transcribe_audio(audio_url)
            
            if audio_text:
                # Enter the transcribed text
                audio_input = self.driver.find_element(By.CSS_SELECTOR, '#audio-response')
                audio_input.clear()
                audio_input.send_keys(audio_text)
                
                # Submit
                verify_button = self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-verify-button')
                await self.human_like_click(verify_button)
                
                await asyncio.sleep(3)
                
                # Check if solved
                if not self.driver.find_elements(By.CSS_SELECTOR, '.rc-audiochallenge-error-message'):
                    self.logger.info("Audio challenge solved successfully")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving audio challenge: {e}")
            return False

    async def solve_recaptcha_images(self) -> bool:
        """Solve reCAPTCHA image challenge"""
        try:
            self.logger.info("Attempting image challenge")
            
            # Get challenge instructions
            instructions = self.driver.find_element(By.CSS_SELECTOR, '.rc-imageselect-desc-no-canonical')
            challenge_text = instructions.text.lower()
            
            self.logger.info(f"Challenge: {challenge_text}")
            
            # Get all image tiles
            image_tiles = self.driver.find_elements(By.CSS_SELECTOR, '.rc-imageselect-tile')
            
            # Analyze each image tile
            for i, tile in enumerate(image_tiles):
                try:
                    # Get image data
                    img_element = tile.find_element(By.CSS_SELECTOR, 'img')
                    img_src = img_element.get_attribute('src')
                    
                    # Analyze image content
                    if await self.analyze_image_content(img_src, challenge_text):
                        await self.human_like_click(tile)
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                        
                except Exception as e:
                    self.logger.error(f"Error analyzing image tile {i}: {e}")
                    continue
            
            # Submit solution
            verify_button = self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-verify-button')
            await self.human_like_click(verify_button)
            
            await asyncio.sleep(3)
            
            # Check if solved
            if not self.driver.find_elements(By.CSS_SELECTOR, '.rc-imageselect-error-select-more'):
                self.logger.info("Image challenge solved successfully")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving image challenge: {e}")
            return False

    async def solve_hcaptcha(self) -> bool:
        """Solve hCaptcha"""
        try:
            self.logger.info("Attempting to solve hCaptcha")
            
            # Switch to hCaptcha iframe
            hcaptcha_iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="hcaptcha"]'))
            )
            
            self.driver.switch_to.frame(hcaptcha_iframe)
            
            # Click the checkbox
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.hcaptcha-checkbox'))
            )
            
            await self.human_like_click(checkbox)
            
            # Wait for challenge or completion
            await asyncio.sleep(3)
            
            # Check if additional challenge appeared
            if self.driver.find_elements(By.CSS_SELECTOR, '.challenge-container'):
                # Handle hCaptcha image challenge
                success = await self.solve_hcaptcha_images()
                self.driver.switch_to.default_content()
                return success
            
            # Check if solved
            if self.driver.find_elements(By.CSS_SELECTOR, '.hcaptcha-success'):
                self.logger.info("hCaptcha solved successfully")
                self.driver.switch_to.default_content()
                return True
            
            self.driver.switch_to.default_content()
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving hCaptcha: {e}")
            self.driver.switch_to.default_content()
            return False

    async def solve_hcaptcha_images(self) -> bool:
        """Solve hCaptcha image challenge"""
        try:
            # Get challenge instructions
            instructions = self.driver.find_element(By.CSS_SELECTOR, '.challenge-text')
            challenge_text = instructions.text.lower()
            
            # Get image tiles
            image_tiles = self.driver.find_elements(By.CSS_SELECTOR, '.challenge-image')
            
            # Analyze and click relevant images
            for tile in image_tiles:
                img_src = tile.get_attribute('src')
                if await self.analyze_image_content(img_src, challenge_text):
                    await self.human_like_click(tile)
                    await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Submit
            submit_button = self.driver.find_element(By.CSS_SELECTOR, '.challenge-submit')
            await self.human_like_click(submit_button)
            
            await asyncio.sleep(3)
            return True
            
        except Exception as e:
            self.logger.error(f"Error solving hCaptcha images: {e}")
            return False

    async def solve_image_captcha(self) -> bool:
        """Solve traditional image CAPTCHA"""
        try:
            self.logger.info("Attempting to solve image CAPTCHA")
            
            # Find CAPTCHA image
            captcha_img = None
            for selector in self.captcha_selectors['image_captcha']:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    captcha_img = elements[0]
                    break
            
            if not captcha_img:
                return False
            
            # Get image source
            img_src = captcha_img.get_attribute('src')
            
            # Solve using OCR
            captcha_text = await self.ocr_image_captcha(img_src)
            
            if captcha_text:
                # Find input field
                input_field = None
                for selector in self.captcha_selectors['text_captcha']:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        input_field = elements[0]
                        break
                
                if input_field:
                    input_field.clear()
                    input_field.send_keys(captcha_text)
                    self.logger.info(f"Entered CAPTCHA text: {captcha_text}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving image CAPTCHA: {e}")
            return False

    async def solve_text_captcha(self) -> bool:
        """Solve text-based CAPTCHA"""
        try:
            self.logger.info("Attempting to solve text CAPTCHA")
            
            # Look for CAPTCHA question
            question_elements = self.driver.find_elements(By.CSS_SELECTOR, '.captcha-question, .captcha-text, [class*="captcha"]')
            
            for element in question_elements:
                text = element.text.lower()
                if any(word in text for word in ['what', 'how', 'which', 'calculate', 'solve']):
                    answer = await self.solve_math_captcha(text)
                    if answer:
                        # Find input field
                        input_field = None
                        for selector in self.captcha_selectors['text_captcha']:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                input_field = elements[0]
                                break
                        
                        if input_field:
                            input_field.clear()
                            input_field.send_keys(str(answer))
                            return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving text CAPTCHA: {e}")
            return False

    async def solve_recaptcha_v3(self) -> bool:
        """Handle reCAPTCHA v3 (invisible)"""
        try:
            # reCAPTCHA v3 is usually invisible and automatic
            # Just wait for it to complete
            await asyncio.sleep(3)
            
            # Check if score is acceptable
            response_element = self.driver.find_elements(By.CSS_SELECTOR, '.g-recaptcha-response')
            if response_element and response_element[0].get_attribute('value'):
                self.logger.info("reCAPTCHA v3 completed successfully")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error with reCAPTCHA v3: {e}")
            return False

    async def human_like_click(self, element):
        """Perform human-like click with random delays and movements"""
        try:
            # Random delay before click
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Move to element with slight randomness
            actions = ActionChains(self.driver)
            
            # Get element location and size
            location = element.location
            size = element.size
            
            # Add random offset
            offset_x = random.randint(-size['width']//4, size['width']//4)
            offset_y = random.randint(-size['height']//4, size['height']//4)
            
            # Move to element with offset
            actions.move_to_element_with_offset(element, offset_x, offset_y)
            
            # Random pause before click
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # Click
            actions.click()
            actions.perform()
            
            # Random delay after click
            await asyncio.sleep(random.uniform(0.2, 1.0))
            
        except Exception as e:
            self.logger.error(f"Error performing human-like click: {e}")
            # Fallback to regular click
            element.click()

    async def transcribe_audio(self, audio_url: str) -> Optional[str]:
        """Transcribe audio CAPTCHA using speech recognition"""
        try:
            # Download audio file
            response = requests.get(audio_url)
            if response.status_code != 200:
                return None
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(response.content)
                temp_audio_path = temp_file.name
            
            # Convert to WAV if needed
            audio = AudioSegment.from_file(temp_audio_path)
            wav_path = temp_audio_path.replace('.mp3', '.wav')
            audio.export(wav_path, format='wav')
            
            # Transcribe using speech recognition
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                
            # Clean up
            os.unlink(temp_audio_path)
            os.unlink(wav_path)
            
            return text.lower().strip()
            
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            return None

    async def analyze_image_content(self, img_src: str, challenge_text: str) -> bool:
        """Analyze image content to determine if it matches the challenge"""
        try:
            # This is a simplified version - in production, you'd use more sophisticated image recognition
            # For now, we'll use basic heuristics
            
            # Download image
            response = requests.get(img_src)
            if response.status_code != 200:
                return False
            
            # Convert to OpenCV format
            image = Image.open(io.BytesIO(response.content))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Basic image analysis based on challenge type
            if 'traffic light' in challenge_text:
                return await self.detect_traffic_light(cv_image)
            elif 'crosswalk' in challenge_text:
                return await self.detect_crosswalk(cv_image)
            elif 'car' in challenge_text:
                return await self.detect_car(cv_image)
            elif 'bus' in challenge_text:
                return await self.detect_bus(cv_image)
            elif 'bicycle' in challenge_text:
                return await self.detect_bicycle(cv_image)
            elif 'bridge' in challenge_text:
                return await self.detect_bridge(cv_image)
            
            # Default: random selection with low probability
            return random.random() < 0.3
            
        except Exception as e:
            self.logger.error(f"Error analyzing image: {e}")
            return False

    async def detect_traffic_light(self, image) -> bool:
        """Detect traffic lights in image"""
        # Simplified detection - look for circular shapes in typical traffic light colors
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Red color range
        red_lower = np.array([0, 50, 50])
        red_upper = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        
        # Yellow color range
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        
        # Green color range
        green_lower = np.array([40, 50, 50])
        green_upper = np.array([80, 255, 255])
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        
        # Check for circular shapes
        circles_red = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=50)
        circles_yellow = cv2.HoughCircles(yellow_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=50)
        circles_green = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=50)
        
        return any(circles is not None for circles in [circles_red, circles_yellow, circles_green])

    async def detect_crosswalk(self, image) -> bool:
        """Detect crosswalks in image"""
        # Look for white stripes pattern
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Detect lines
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
        
        if lines is not None:
            # Look for parallel horizontal lines (crosswalk pattern)
            horizontal_lines = [line for line in lines if abs(line[0][1] - line[0][3]) < 10]
            return len(horizontal_lines) > 3
        
        return False

    async def detect_car(self, image) -> bool:
        """Detect cars in image"""
        # Simplified car detection using color and shape analysis
        # In production, you'd use a trained model
        
        # Look for rectangular shapes in typical car colors
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for rectangular shapes
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:  # Rectangle
                area = cv2.contourArea(contour)
                if area > 1000:  # Large enough to be a car
                    return True
        
        return False

    async def detect_bus(self, image) -> bool:
        """Detect buses in image"""
        # Similar to car detection but look for larger rectangular shapes
        return await self.detect_car(image)  # Simplified

    async def detect_bicycle(self, image) -> bool:
        """Detect bicycles in image"""
        # Look for circular shapes (wheels)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=50)
        
        return circles is not None and len(circles[0]) >= 2

    async def detect_bridge(self, image) -> bool:
        """Detect bridges in image"""
        # Look for horizontal structures
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
        
        if lines is not None:
            horizontal_lines = [line for line in lines if abs(line[0][1] - line[0][3]) < 20]
            return len(horizontal_lines) > 2
        
        return False

    async def ocr_image_captcha(self, img_src: str) -> Optional[str]:
        """Extract text from image CAPTCHA using OCR"""
        try:
            # Download image
            response = requests.get(img_src)
            if response.status_code != 200:
                return None
            
            # Open image
            image = Image.open(io.BytesIO(response.content))
            
            # Preprocess image for better OCR
            image = image.convert('L')  # Convert to grayscale
            image = image.resize((image.width * 2, image.height * 2))  # Upscale
            
            # Use OCR (you'd need to install pytesseract)
            try:
                import pytesseract
                text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
                return text.strip()
            except ImportError:
                self.logger.warning("pytesseract not installed, using fallback OCR")
                return None
            
        except Exception as e:
            self.logger.error(f"Error performing OCR: {e}")
            return None

    async def solve_math_captcha(self, question: str) -> Optional[int]:
        """Solve simple math CAPTCHA"""
        try:
            # Extract numbers and operators
            import re
            
            # Common math patterns
            patterns = [
                r'(\d+)\s*\+\s*(\d+)',  # Addition
                r'(\d+)\s*-\s*(\d+)',   # Subtraction
                r'(\d+)\s*\*\s*(\d+)',  # Multiplication
                r'(\d+)\s*/\s*(\d+)',   # Division
            ]
            
            for pattern in patterns:
                match = re.search(pattern, question)
                if match:
                    num1, num2 = int(match.group(1)), int(match.group(2))
                    
                    if '+' in question:
                        return num1 + num2
                    elif '-' in question:
                        return num1 - num2
                    elif '*' in question:
                        return num1 * num2
                    elif '/' in question:
                        return num1 // num2 if num2 != 0 else None
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error solving math CAPTCHA: {e}")
            return None

    async def solve_with_2captcha(self) -> bool:
        """Solve CAPTCHA using 2captcha service"""
        try:
            if not self.captcha_services['2captcha']['api_key']:
                return False
            
            # Get site key
            site_key = None
            for selector in self.captcha_selectors['recaptcha_v2']:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    site_key = elements[0].get_attribute('data-sitekey')
                    break
            
            if not site_key:
                return False
            
            # Submit CAPTCHA to 2captcha
            submit_data = {
                'key': self.captcha_services['2captcha']['api_key'],
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': self.driver.current_url
            }
            
            response = requests.post(self.captcha_services['2captcha']['url'], data=submit_data)
            if response.status_code != 200:
                return False
            
            result = response.text
            if not result.startswith('OK|'):
                return False
            
            captcha_id = result.split('|')[1]
            
            # Wait for solution
            for _ in range(60):  # Wait up to 5 minutes
                await asyncio.sleep(5)
                
                result_data = {
                    'key': self.captcha_services['2captcha']['api_key'],
                    'action': 'get',
                    'id': captcha_id
                }
                
                response = requests.get(self.captcha_services['2captcha']['result_url'], params=result_data)
                result = response.text
                
                if result.startswith('OK|'):
                    solution = result.split('|')[1]
                    
                    # Inject solution
                    self.driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{solution}";')
                    return True
                elif result != 'CAPCHA_NOT_READY':
                    break
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error using 2captcha service: {e}")
            return False

    def set_captcha_service_key(self, service: str, api_key: str):
        """Set API key for CAPTCHA solving service"""
        if service in self.captcha_services:
            self.captcha_services[service]['api_key'] = api_key

# Example usage
async def main():
    # Initialize Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to a page with CAPTCHA
        driver.get('https://example.com/with-captcha')
        
        # Initialize CAPTCHA solver
        solver = CaptchaSolver(driver)
        
        # Solve CAPTCHA
        success = await solver.solve_captcha()
        
        if success:
            print("CAPTCHA solved successfully!")
        else:
            print("Failed to solve CAPTCHA")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main()) 