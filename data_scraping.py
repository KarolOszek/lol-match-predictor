from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://gol.gg/teams/list/season-ALL/split-ALL/tournament-LPL%202026%20Split%203/")
time.sleep(2)
driver.find_element(By.CLASS_NAME, 'fc-button.fc-cta-consent.fc-primary-button').click()

def scrape():
    data_from_table = driver.find_elements(By.TAG_NAME, 'table')[1].text
    return data_from_table


tables = []
elements = driver.find_elements(By.CLASS_NAME, "tablesaw-cell-persist")

for i in range(1, len(elements)):
    elements = driver.find_elements(By.CLASS_NAME, "tablesaw-cell-persist")
    elements[i].find_element(By.TAG_NAME, 'a').click()
    categories = driver.find_elements(By.CLASS_NAME, "navbar-nav.mr-auto.mt-2.mt-lg-0")
    match_history = categories[1].find_element(By.XPATH, "//a[text()='Match list']")
    match_history.click()
    tables.append(scrape())
    driver.get("https://gol.gg/teams/list/season-ALL/split-ALL/tournament-LPL%202026%20Split%203/")

print(tables)
