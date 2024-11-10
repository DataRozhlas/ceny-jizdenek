#!/usr/bin/

import os
from time import sleep
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

kam = f"downloads/{datetime.now().strftime('%Y-%m-%d')}"
os.makedirs(kam, exist_ok=True)

def regiojet(odkud, kam, pocet_dni=0):

    def uloz_stranku(pocet_dni):
            with open(
                os.path.join(
                    f"downloads/{datetime.now().strftime('%Y-%m-%d')}",
                    f"rj_{odkud}_{kam}_D{pocet_dni:02}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html",
                ),
                "w+",
                encoding="utf-8",
            ) as ven:
                ven.write(driver.page_source)

            print(f"Uloženo: {odkud}-{kam} {pocet_dni} D")

    try:

        display = Display(visible=0, size=(1920, 1080))
        display.start()
        
        print("Startuji.")

        driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")

        print("Driver načten.")

        print("Otevírám regiojet.cz.")

        driver.get("https://regiojet.cz/")

        print("Regiojet otevřen.")

        wait = WebDriverWait(driver, 10)

        pole1 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Odkud']"))
        )

        print("Vyťukávám ODKUD.")

        pole1.send_keys(odkud)

        print("Vyťukáno ODKUD.")

        pole1.send_keys(Keys.ENTER)

        sleep(random.randint(4, 5))
        pole2 = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Kam']"))
        )

        print("Vyťukávám KAM.")

        pole2.send_keys(kam)
        sleep(random.randint(3, 4))
        pole2.send_keys(Keys.ENTER)
        sleep(random.randint(3, 4))

        print("Posílám druhý ENTER.")

        pole2.send_keys(Keys.ENTER)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        sleep(random.randint(3, 4))

        uloz_stranku(pocet_dni=0)

        for den in range(1, 60):
                            
            driver.execute_script(
                """document.querySelectorAll('.max-h-screen').forEach(element => element.style.display = 'none');"""
            )
            dalsi =  driver.find_element(By.XPATH, "//button[text()='Další spoje']")
            sleep(random.randint(3, 6))
            
            print("Klikám na další spojení.")
            
            dalsi.click()
            uloz_stranku(pocet_dni=den)

    except Exception as e:
        print(e)

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(e)
        if display:
            try:
                display.stop()
            except Exception as e:
                print(e)

trasy_a = [('Praha','Brno'),
           ('Praha','Ostrava')]

trasy_b = [
     ('Olomouc','Przemysl'),
     ('Kolín','Ústí nad Labem'),
     ('Ostrava','Brno'),
     ('Brno','Vídeň'),
     ('Praha','Budapešť'),
     ('Praha','Košice'),
     ('Praha','Čop'),
     ('Praha','Vídeň'),
     ('Praha','Bratislava'),
     ('Praha','Krakov')
]

random.shuffle(trasy_b)
trasy = trasy_a + trasy_b[:3]
random.shuffle(trasy)

for t in trasy:
    regiojet(t[0],t[1])
    regiojet(t[1],t[0])