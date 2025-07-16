from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlsxwriter
import re
from collections import Counter

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
    pattern = re.compile(r'(Application viewed|Applied) (\d+)(h|d|w|mo|yr) ago')

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
    worksheet = workbook.add_worksheet('Full Application Data')

    worksheet.write('A1', 'Job Title')
    worksheet.write('B1', 'Company Name')
    worksheet.write('C1', 'Time Since Application')
    worksheet.write('D1', 'Application Viewed (Y/N)')

    for row_number in range(2, len(job_titles)):
        job_title_cell = 'A'+str(row_number)
        company_name_cell = 'B'+str(row_number)
        time_since_app_cell = 'C'+str(row_number)
        app_viewed_cell = 'D'+str(row_number)
        try:
            worksheet.write(job_title_cell, job_titles[row_number-2])
        except:
            print('There are no more job titles')
        try:
            worksheet.write(company_name_cell, company_names[row_number-2])
        except:
            print('There are no more companies')
        try:
            worksheet.write(time_since_app_cell, time_since_applications[row_number-2])
        except:
            print('There are no more times since applications')
        try:
            worksheet.write(app_viewed_cell, application_views[row_number-2])
        except:
            print('There are no more view flags')

    create_application_views_bar_graph()
    create_application_timeline_line_graph()
    workbook.close()
        

def create_application_views_bar_graph():

    application_viewed_count = application_views.count('y')
    application_not_viewed_count = application_views.count('n')

    #adding data
    worksheet = workbook.add_worksheet('Applications_Viewed_Bar_Graph')
    worksheet.write('A1', 'Status')
    worksheet.write('B1', 'Count')
    worksheet.write('A2', 'Viewed')
    worksheet.write('B2', application_viewed_count)
    worksheet.write('A3', 'Not viewed')
    worksheet.write('B3', application_not_viewed_count)

    #creating chart
    chart = workbook.add_chart({'type': 'column'})

    chart.add_series({
    'name':       'Application Status',
    'categories': '=Applications_Viewed_Bar_Graph!$A$2:$A$3',
    'values':     '=Applications_Viewed_Bar_Graph!$B$2:$B$3',
    })

    # add chart title and axis labels
    chart.set_title({'name': 'Job Application Views'})
    chart.set_x_axis({'name': 'Status'})
    chart.set_y_axis({'name': 'Number of Jobs'})

    # insert chart into worksheet
    worksheet.insert_chart('D2', chart)

def create_application_timeline_line_graph():

    worksheet = workbook.add_worksheet('Applications_Timeline_Graph')
    
    #regex for timeline
    pattern = re.compile(r'^(\d+)(h|d|w|mo|yr)$')

    #weighting time units
    time_weights = {'h': 1, 'd': 24, 'w': 168, 'mo': 720, 'yr': 8760}

    parsed_times = []
    for entry in time_since_applications:
        if entry == 'unknown':
            continue
        match = pattern.match(entry)
        if match:
            value, unit = match.groups()
            value = int(value)
            hours = value * time_weights[unit]
            parsed_times.append((entry, hours))

    labels_only = [label for label, _ in parsed_times]
    counts = Counter(labels_only)

    # sort times chronologically
    sorted_items = sorted(counts.items(), key=lambda item: int(pattern.match(item[0]).group(1)) * time_weights[pattern.match(item[0]).group(2)])

    worksheet.write('A1', 'Time Since Application')
    worksheet.write('B1', 'Number of Applications')

    
    for row, (label, count) in enumerate(sorted_items, start=1):
        worksheet.write(row, 0, label)
        worksheet.write(row, 1, count)

    
    chart = workbook.add_chart({'type': 'line'})

    chart.add_series({
        'name': 'Applications Over Time',
        'categories': f'=Applications_Timeline_Graph!$A$2:$A${len(sorted_items)+1}',
        'values':     f'=Applications_Timeline_Graph!$B$2:$B${len(sorted_items)+1}',
        'marker': {'type': 'circle'},
        'line': {'color': 'blue'}
    })


    chart.set_title({'name': 'Job Applications Over Time'})
    chart.set_x_axis({'name': 'Time Since Application'})
    chart.set_y_axis({'name': 'Number of Applications'})

    worksheet.insert_chart('D2', chart)

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

#establish lists that will be output to excel
job_titles = []
company_names = []
time_since_applications = []
application_views = []

#initialise excel workbook
workbook_name = "LinkedIn Application Data.xlsx"
workbook = xlsxwriter.Workbook(workbook_name)

run_linkedin_scraper()
c
