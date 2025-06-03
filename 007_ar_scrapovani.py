#!/usr/bin/

import os
import random
from time import sleep
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

def arriva(odkud, kam):

    def uloz_stranku(pocet_dni):
        with open(
            os.path.join(
                f"downloads/{datetime.now().strftime('%Y-%m-%d')}",
                f"ar_{odkud}_{kam}_D{pocet_dni}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html",
            ),
            "w+",
            encoding="utf-8",
        ) as ven:
            ven.write(driver.page_source)

        print(f"Uloženo: {odkud}-{kam} {pocet_dni} D")

    try:

        display = Display(visible=0, size=(1920, 1080))
        display.start()

        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.get("https://jizdenky.arriva.cz/")

        print("Otevírám stránky.")

        wait = WebDriverWait(driver, 10)
        from_input = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "suggest-input-from"))
        )
        from_input.clear()
        from_input.send_keys(odkud)
        print("Odkud vyplněno.")
        sleep(2)
        from_input.send_keys(Keys.TAB)
        sleep(2)
        to_input = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "suggest-input-to"))
        )
        to_input.send_keys(kam)
        print("Kam vyplněno")
        sleep(2)
        to_input.send_keys(Keys.TAB)
        sleep(2)

        submit_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[type='submit']"))
        )

        sleep(2)
        submit_button.click()

        print("Odkliknuto.")

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        uloz_stranku(0)

        for i in range(1, random.randint(7, 31)):
            dalsi = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button.btn.icon.size-m.secondary")
                )
            )
            sleep(1)
            dalsi[1].click()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            uloz_stranku(i)

    except Exception as E:
        print(E)

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as E:
                print(E)
        if display:
            try:
                display.stop()
            except Exception as e:
                print(e)


trasy = [
    ("Praha", "Tanvald"),
    ("Praha", "České Budějovice"),
    ("Pardubice", "Liberec"),
    ("Liberec", "Pardubice"),
    ("Ústí nad Labem", "Liberec")
]

random.shuffle(trasy)
trasy = trasy[0]

for t in trasy:
    arriva(t[0], t[1])
    arriva(t[1], t[0])
