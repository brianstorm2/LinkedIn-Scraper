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

job_title = []
company_name = []
days_since_application = []

job = driver.find_elements(By.CSS_SELECTOR  , '[entity-result__title-text]')
print(job)
