#!/usr/bin/

import os
from time import sleep
import requests
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

kam = f"downloads/{datetime.now().strftime("%Y-%m-%d")}"
os.makedirs(kam, exist_ok=True)

def cd(odkud, kam):

    try:
        driver = webdriver.Firefox()
        driver.get("https://www.cd.cz/") 
        sleep(10)

        button = driver.find_element(By.XPATH, "//button[text()='Povolit všechny soubory cookie']")
        button.click()

        wait = WebDriverWait(driver, 10)
        from_input = wait.until(EC.presence_of_element_located((By.ID, "connection-from")))
        from_input.clear()
        from_input.send_keys(odkud)
        to_input = wait.until(EC.presence_of_element_located((By.ID, "connection-to")))
        to_input.clear()
        to_input.send_keys(kam)
        
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-btn")))
        search_button.click()
        
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        sleep(2)
        
        with open(os.path.join(f"downloads/{datetime.now().strftime("%Y-%m-%d")}",f"cd_{odkud}_{kam}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt"), "w+", encoding="utf-8") as ven:
            ven.write(driver.page_source)
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

trasy = [
    ('Praha','Brno'),
    ('Brno','Praha'),
    ('Praha','Ostrava'),
    ('České Budějovice','Plzeň'),
    ('Karlovy Vary','Děčín'),
    ('Znojmo','Frýdek-Místek'),
    ('Ostrava','Varšava'),
    ('Plzeň','Bratislava'),
    ('Olomouc', 'Berlín'),
    ('Liberec','Vídeň')
]

for x in trasy:
    cd(x[0],x[1])