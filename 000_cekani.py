#!/usr/bin/

from time import sleep
import random

doba = random.randint(0, 3600)

print(f"Nýčko budeme čekat {doba} sekund.")

with open("001_log.txt", "w+", encoding="utf-8") as log:
    log.write(f"{doba} s")

sleep(doba)

print("A do práce!")