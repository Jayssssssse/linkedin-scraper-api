from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = FastAPI(title="LinkedIn Scraper API")

def login_linkedin(driver):
    """Login to LinkedIn using credentials from environment variables"""
    try:
        # Get credentials from environment
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')
        
        if not email or not password:
            print("Warning: LinkedIn credentials not found in environment")
            return False
        
        # Navigate to LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)
        
        # Enter email
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(email)
        
        # Enter password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for login to complete
        time.sleep(5)
        
        return True
    except Exception as e:
        time.sleep(10)  # Wait longer after login to avoid detection
class LinkedInProfile(BaseModel):
    profile_url: str

@app.get("/")
async def root():
    return {"message": "LinkedIn Scraper API - Ready", "status": "active"}

@app.post("/scrape")
async def scrape_linkedin(profile: LinkedInProfile):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_
                                          chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)options)
        driver.get(profile.profile_url)
        time.sleep(3)
        
        # Basic scraping - get page title
                
        # Login to LinkedIn
        login_success = login_linkedin(driver)
        if not login_success:
            print("Warning: LinkedIn login failed, continuing without auth")
                
        # Extract profile data from LinkedIn page
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException
        
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Extract name
            try:
                name_element = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge")
                full_name = name_element.text.strip()
            except NoSuchElementException:
                full_name = ""
            
            # Extract headline/title
            try:
                headline_element = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium")
                headline = headline_element.text.strip()
            except NoSuchElementException:
                headline = ""
            
            # Extract location
            try:
                location_element = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light.break-words")
                location = location_element.text.strip()
            except NoSuchElementException:
                location = ""
            
            # Extract current company (from experience section)
            try:
                company_element = driver.find_element(By.CSS_SELECTOR, "#experience + div div.display-flex.flex-column.full-width div.display-flex.flex-column div span[aria-hidden='true']")
                company_name = company_element.text.strip()
            except NoSuchElementException:
                company_name = ""
        except Exception as e:
            print(f"Error extracting profile data: {e}")
            full_name = ""
            headline = ""
            location = ""
            company_name = ""
        title = driver.title
        
        driver.quit()
        
        return {
            "status": "success",
            "url": profile.profile_url,
            "page_title": title,
                        "fullName": full_name,
            "headline": headline,
            "location": location,
            "companyName": company_name,
            "profileUrl": profile.profile_url,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
