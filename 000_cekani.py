#!/usr/bin/

from time import sleep
import random

doba = random.randint(0, 3600)

print(f"Nýčko budeme čekat {doba} sekund.")

sleep(doba)

print("A do práce!")