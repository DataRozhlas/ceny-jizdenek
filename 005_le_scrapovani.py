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

def leo(odkud1, odkud2, kam1, kam2, pocet_dni):

    try:

        display = Display(visible=0, size=(1920, 1080))
        display.start()
#        driver = webdriver.Chrome()

        driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")

        sablona = "https://www.leoexpress.com/cs/vysledky-vyhledavani?date=KDY_POJEDEME&from=MISTO_ODKUD1&fromCountry=&fromName=MISTO_ODKUD2&persons=%5B%7B%22adult%22%3A%5B%5D%2C%22combine%22%3A1%2C%22count%22%3A1%2C%22parentTariffs%22%3Anull%7D%5D&returnDate=&services=%5B%7B%22service_id%22%3A%223%22%2C%22count%22%3A0%7D%2C%7B%22service_id%22%3A%224%22%2C%22count%22%3A0%7D%5D&to=MISTO_KAM1&toCountry=&toName=MISTO_KAM2&toggleDiscounts=false"""
        den = data(pocet_dni)
        url = sablona.replace('KDY_POJEDEME',den).replace('MISTO_ODKUD1',odkud1).replace('MISTO_ODKUD2',odkud2).replace('MISTO_KAM1',kam1).replace('MISTO_KAM2',kam2)

        slozka = f"downloads/{datetime.now().strftime('%Y-%m-%d')}"
        os.makedirs(slozka, exist_ok=True)
        
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        sleep(random.randint(4, 6))

        try:
            driver.execute_script(
            """document.getElementById('CybotCookiebotDialog').style.display = 'none';"""
            )
        except:
            pass

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[text()='Přímý spoj']"))
        )
        element.click()

        try:

            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Přímý spoj')]")
            for element in elements[1:]:
                sleep(1)
                element.click()

        except:
            pass

        print("Dál už to nejde.")

        with open(
            os.path.join(
                slozka,
                f"le_{odkud2}_{kam2}_D{pocet_dni:02}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html",
            ),
            "w+",
            encoding="utf-8",
        ) as ven:
            ven.write(driver.page_source)

        print(f"Uloženo: {odkud2}-{kam2} {pocet_dni} D")

    except Exception as E:
        print(E)

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

def data(days):
    future_date = date.today() + timedelta(days=days)
    formatted_date = future_date.strftime("%d.%m.%Y")
    return formatted_date

odstup = [0, 1, 2, 3]
odstup.append(random.randint(4, 7))
odstup.append(random.randint(8, 15))
odstup.append(random.randint(16, 30))
odstup.append(random.randint(31, 90))
odstup

trasy = [
    (['5457076','Praha'],['OSTRAVA','Ostrava'])
    ]

trasy_b = [(['5457076','Praha'],['5100028','Krak%C3%B3w%20G%C5%82%C3%B3wny']),
    (['PARDUBICE','Pardubice'],['KOSICE','Ko%C5%A1ice'])]

random.shuffle(trasy)
random.shuffle(trasy_b)

trasy = trasy + [trasy_b[0]]

for t in trasy:
    for o in odstup:
        leo(t[0][0], t[0][1], t[1][0], t[1][1], o)
        leo(t[1][0], t[1][1], t[0][0], t[0][1], o)