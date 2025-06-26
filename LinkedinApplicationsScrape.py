from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import xlsxwriter

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
driver.get(url)

job_titles = []
company_names = []
days_since_applications = []

jobs = driver.find_elements(By.CSS_SELECTOR, 'div.t-roman.t-sans')
for job in jobs:
    raw_job_text = str(job.text)
    raw_job_text.replace('\n, Verified', '') #cleaning data
    job_titles.append(raw_job_text)
