#!/usr/bin/

import os
from time import sleep
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

kam = f"downloads/{datetime.now().strftime('%Y-%m-%d')}"
os.makedirs(kam, exist_ok=True)


def cd(odkud, kam, pocet_dni=0):

    print(f"{odkud}-{kam} {pocet_dni} d")

    try:

        display = Display(visible=0, size=(1920, 1080))
        display.start()
        driver = webdriver.Chrome()

        driver.get("https://www.cd.cz/spojeni-a-jizdenka/")
        sleep(2)

        button = driver.find_element(
            By.XPATH, "//button[text()='Povolit všechny soubory cookie']"
        )
        button.click()

        print("Cookies povoleny.")

        wait = WebDriverWait(driver, 10)
        from_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-og-type='from']"))
        )
        from_input.clear()
        from_input.send_keys(odkud)
        to_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-og-type='to']"))
        )
        to_input.clear()
        to_input.send_keys(kam)

        print("Formulář vyplněn.")

        if pocet_dni > 0:

            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "suggestion-options__link")
                )
            )

            driver.execute_script(
                """document.querySelectorAll('.suggestion-options__link').forEach(element => element.style.display = 'none');"""
            )  ## zakryje element zakrývající posouvadlo dní

            kalendar = wait.until(EC.presence_of_element_located((By.ID, "nextday")))
            for i in range(0, pocet_dni):
                sleep(0.25)
                kalendar.click()
            print("Dny zaklikány.")

        odeslat = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-btn"))
        )
        odeslat.click()
        print("Formulář odeslán.")

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        print("Výsledky načteny.")

        for i in range(1, 7):
            nacist = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a.btn--blue[title='+ 5 dalších']")
                )
            )  ## Tohle i u PRG-BRN stačí na následujících 24 hodin.
            sleep(1)
            nacist.click()

            print("Další výsledky naklikány.")

        sleep(1)

        with open(
            os.path.join(
                f"downloads/{datetime.now().strftime('%Y-%m-%d')}",
                f"cd_{odkud}_{kam}_D{pocet_dni:02}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html",
            ),
            "w+",
            encoding="utf-8",
        ) as ven:
            ven.write(driver.page_source)

        print("Výstup uložen.")

        driver.quit()

    except Exception as e:
        print(
            f"Projáníčka, propáníčka, pro ztracené korále – máme všichni namále: {e}."
        )

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(
                    f"Projáníčka, propáníčka, pro ztracené korále – máme všichni namále: {e}."
                )
        if display:
            try:
                display.stop()
            except Exception as e:
                print(
                    f"Projáníčka, propáníčka, pro ztracené korále – máme všichni namále: {e}."
                )

trasy_a = [("Praha", "Brno"), ("Praha", "Ostrava")]

trasy_b = [
    ("Praha", "Brusel"),
    ("Praha", "Berlin"),
    ("Praha", "Budapešť"),
    ("Praha", "Vídeň"),
    ("Praha", "Bratislava"),
    ("Praha", "Varšava")
]

trasy_c = [
    ("Karlovy Vary", "Ostrava"),
    ("Slavonice", "Plzeň"),
    ("Ústí nad Labem", "Dresden"),
    ("Brno", "Hamburg"),
    ("Brno", "Ljubljana"),
    ("Olomouc", "Przemysl"),
    ("Ostrava", "Gdaňsk"),
    ("Pardubice", "Košice"),
    ("Praha", "Bern"),
    ("České Budějovice", "Zürich"),
    ("Praha", "Záhřeb"),
    ("Praha", "Lublaň"),
    ("Praha", "Amsterdam")
]

random.shuffle(trasy_b)
random.shuffle(trasy_c)

trasy = trasy_a + trasy_b[0:2] + trasy_c[0]

dny = [0, 1, 2, 3, 4]
dny.append(random.randint(5, 7))
dny.append(random.randint(8, 10))
dny.append(random.randint(11, 15))
dny.append(random.randint(16, 30))
dny.append(random.randint(31, 90))

random.shuffle(trasy)

for d in dny:
    for x in trasy:
        cd(x[0], x[1], pocet_dni=d)
        cd(x[1], x[0], pocet_dni=d)
