from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = FastAPI(title="LinkedIn Scraper API")

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
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(profile.profile_url)
        time.sleep(3)
        
        # Basic scraping - get page title
        title = driver.title
        
        driver.quit()
        
        return {
            "status": "success",
            "url": profile.profile_url,
            "page_title": title,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
