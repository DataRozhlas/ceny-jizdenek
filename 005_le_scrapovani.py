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

def leo(odkud, kam, pocet_dni):

    try:

        display = Display(visible=0, size=(1920, 1080))
        display.start()
        driver = webdriver.Chrome()
    
        sablona = "https://www.leoexpress.com/cs/vysledky-vyhledavani?date=KDY_POJEDEME&from=MISTO_ODKUD1&fromCountry=&fromName=MISTO_ODKUD2&persons=%5B%7B%22adult%22%3A%5B%5D%2C%22combine%22%3A1%2C%22count%22%3A1%2C%22parentTariffs%22%3Anull%7D%5D&returnDate=&services=%5B%7B%22service_id%22%3A%223%22%2C%22count%22%3A0%7D%2C%7B%22service_id%22%3A%224%22%2C%22count%22%3A0%7D%5D&to=MISTO_KAM1&toCountry=&toName=MISTO_KAM2&toggleDiscounts=false"""
        den = data(pocet_dni)
        url = sablona.replace('KDY_POJEDEME',den).replace('MISTO_ODKUD1',odkud.upper()).replace('MISTO_ODKUD2',odkud).replace('MISTO_KAM1',kam.upper()).replace('MISTO_KAM2',kam)

        slozka = f"downloads/{datetime.now().strftime('%Y-%m-%d')}"
        os.makedirs(slozka, exist_ok=True)
        
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        sleep(random.randint(4, 6))

        with open(
            os.path.join(
                slozka,
                f"le_{odkud}_{kam}_D{pocet_dni:02}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html",
            ),
            "w+",
            encoding="utf-8",
        ) as ven:
            ven.write(driver.page_source)

        print(f"Uloženo: {odkud}-{kam} {pocet_dni} D")

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
    formatted_date = future_date.strftime("%d.%m.%Y")  # Change "." to "-" for DD-MM-YYYY
    return formatted_date

odstup = [0, 1, 2, 3, 4]
odstup.append(random.randint(5, 7))
odstup.append(random.randint(8, 10))
odstup.append(random.randint(11, 15))
odstup.append(random.randint(16, 30))
odstup.append(random.randint(31, 90))
odstup

trasy = [
    ('Praha','Ostrava'),
    ('Pardubice','Košice')
]

random.shuffle(trasy)

for t in trasy:
    for o in odstup:
        leo(t[0], t[1], o)
        leo(t[1], t[0], o)