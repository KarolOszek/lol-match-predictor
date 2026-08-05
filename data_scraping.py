from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd


def get_teams_data():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://gol.gg/teams/list/season-ALL/split-ALL/tournament-LPL%202026%20Split%203/")

    def scrape():
        data_from_table = driver.find_elements(By.TAG_NAME, 'table')[1].get_attribute('outerHTML')
        return data_from_table


    tables = []
    elements = driver.find_elements(By.CLASS_NAME, "tablesaw-cell-persist")

    for i in range(1, len(elements)):
        elements = driver.find_elements(By.CLASS_NAME, "tablesaw-cell-persist")
        element = elements[i].find_element(By.TAG_NAME, 'a')
        driver.execute_script("arguments[0].click();", element)

        categories = driver.find_elements(By.CLASS_NAME, "navbar-nav.mr-auto.mt-2.mt-lg-0")
        match_history = categories[1].find_element(By.XPATH, "//a[text()='Match list']")
        driver.execute_script("arguments[0].click();", match_history)
        tables.append(scrape())
        driver.get("https://gol.gg/teams/list/season-ALL/split-ALL/tournament-LPL%202026%20Split%203/")

    dfs = []
    for table in tables:
        table_html = pd.read_html(table)
        table_html[0] = table_html[0].rename(columns={'Unnamed: 3':'Kills', 'Unnamed: 4': 'Gold/sec','Unnamed: 5':'Towers','Unnamed: 6':'Dragons', 'Unnamed: 8':'Kills/15 minute', 'Unnamed: 9':'Gold/sec/15 minute', 'Unnamed: 10':'Towers/15 minute', 'Unnamed: 11':'Dragons/15 minute' })
        dfs.append(table_html[0])
    driver.close()
    
    return dfs