from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import xlsxwriter

#visualisations, num of application line graph dates
#pie chart views vs applications

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
driver.get(url)

#establish lists that will be output to excel
job_titles = []
company_names = []
days_since_applications = []

#last page - know how many times to iterate code
last_page_selenium = driver.find_element(By.CSS_SELECTOR, '#ember104 > button')
last_page_number = int(last_page_selenium.text) #converting last page to int

#fetching job titles
jobs = driver.find_elements(By.CSS_SELECTOR, 'div.t-roman.t-sans')
for job in jobs:
    raw_job_text = str(job.text)
    raw_job_text.replace('\n, Verified', '') #cleaning data
    job_titles.append(raw_job_text)

#fetching company names
companies = driver.find_elements(By.CSS_SELECTOR, '.t-14.t-black.t-normal')
for company in companies:
    company_names.append(company.text)

#fetching time since application, sort views as well
days_since_applying = driver.find_elements(By.CSS_SELECTOR, '.reusable-search-simple-insight__text--small')
