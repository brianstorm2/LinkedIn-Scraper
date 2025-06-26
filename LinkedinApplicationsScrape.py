from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlsxwriter

#visualisations, num of application line graph dates
#pie chart views vs applications
#totals in spreadhseet, number of jobs

def run_linkedin_scraper():
    url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
    driver.get(url)

    # Wait for the user to log in and for the last page button to be present
    try:
        wait = WebDriverWait(driver, 120)  # wait up to 120 seconds for login and page load
        last_page_selenium = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#ember104 > button'))
        )
        #last_page, know how many times to iterate
        last_page_number = int(last_page_selenium.text)  # converting last page to int
        end_number_of_applications = (last_page_number * 10) - 10

        collect_job_data()

    except Exception as e:
        print(f"An error occurred: {e}")

    #iterate through each page
    for i in range(10, end_number_of_applications, 10):
        new_url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start="+str(i)
        driver.get(new_url)
        time.sleep(3)
        collect_job_data()

def collect_job_data():
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
    

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

#establish lists that will be output to excel
job_titles = []
company_names = []
days_since_applications = []

run_linkedin_scraper()
