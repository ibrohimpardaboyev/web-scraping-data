from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

url = "https://www.linkedin.com/jobs/search/?keywords=Python%20Developer&location=Worldwide"
driver.get(url)
time.sleep(3)

jobs_data = []

def scroll_and_expand():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            show_more = driver.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button")
            if show_more.is_displayed():
                driver.execute_script("arguments[0].click();", show_more)
                time.sleep(2)
        except:
            pass
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


scroll_and_expand()

job_cards = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list li")

for job in job_cards:
    try:
        title = job.find_element(By.CSS_SELECTOR, "h3").text.strip()
        company = job.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle").text.strip()
        location = job.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
        jobs_data.append({
            "Title": title,
            "Company": company,
            "Location": location
        })
    except Exception:
        continue

driver.quit()

df = pd.DataFrame(jobs_data)
df.to_csv("linkedin_python_developer_jobs.csv", index=False)
