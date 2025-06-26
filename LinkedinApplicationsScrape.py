from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlsxwriter
import re

#visualisations, num of application line graph dates
#pie chart views vs applications
#totals in spreadhseet, number of jobs
#organisations that viewed your application

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
        end_number_of_applications = (last_page_number * 10)
        print(end_number_of_applications)

        collect_job_data()

    except Exception as e:
        print(f"An error occurred: {e}")

    #iterate through each page
    for i in range(10, end_number_of_applications, 10):
        ##go headless
        new_url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start="+str(i)
        driver.get(new_url)
        time.sleep(3)
        collect_job_data()

def collect_job_data():
    #fetching job titles
    jobs = driver.find_elements(By.CSS_SELECTOR, 'div.t-roman.t-sans')
    for job in jobs:
        raw_job_text = str(job.text)
        #data sanitisation
        raw_job_text = re.sub(r'\n?,? Verified', '', raw_job_text)
        raw_job_text = raw_job_text.replace('\n', '')
        job_titles.append(raw_job_text)

    #fetching company names
    companies = driver.find_elements(By.CSS_SELECTOR, '.t-14.t-black.t-normal')
    for company in companies:
        company_names.append(company.text)

    #regex for time since application    
    pattern = re.compile(r'(Application viewed|Applied) (\d+)(h|d|w|mo|y) ago')

    #fetching time since application, sort views as well
    time_since_applying = driver.find_elements(By.CSS_SELECTOR, '.reusable-search-simple-insight__text--small')
    for time in time_since_applying:
        text = time.text
        match = pattern.match(text)
        #if regex matches
        if match:
            status, value, unit = match.groups()
            time_since_applications.append(f"{value}{unit}")
            application_views.append('y' if status == 'Application viewed' else 'n')
        else:
            time_since_applications.append("unknown")
            application_views.append("n")


def export_data_excel():
    workbook_name = "LinkedIn Application Data"
    workbook = xlsxwriter.Workbook(workbook_name)
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Job Title')
    worksheet.write('B1', 'Company Name')
    worksheet.write('C1', 'Time Since Application')
    worksheet.write('D1', 'Application Viewed (Y/N)')

    for row_number in range(2, len(job_titles)):
        job_title_cell = 'A'+str(row_number)
        company_name_cell = 'B'+str(row_number)
        time_since_app_cell = 'C'+str(row_number)
        app_viewed_cell = 'D'+str(row_number)
    

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

#establish lists that will be output to excel
job_titles = []
company_names = []
time_since_applications = []
application_views = []

run_linkedin_scraper()
