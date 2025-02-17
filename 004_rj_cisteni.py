#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
from datetime import datetime
import pandas as pd


# In[2]:


def oscrapuj_rj(slozka, soubor):
    with open(os.path.join(slozka,soubor), "r", encoding="utf-8") as spojeni:
        spojeni = spojeni.read()
    spoje = []
    spoj = None
    for radek in spojeni.split("</"):
        if len(radek) < 5000:
            radek = radek.replace("<sup>+1","")
            if re.search(r"\w{5,12},\s\d{1,2}\.\s\w{4,12}\s20\d\d", radek):
                datum = re.search(r"\w{5,12},\s\d{1,2}\.\s\w{4,12}\s20\d\d", radek).group(0)
                den = datum.split(",")[0]
                datum = datum.split(',')[1].replace("ledna","1.").replace("února","2.").replace("března","3.").replace("dubna","4.").replace("května","5.").replace("června","6.").replace('července','7.').replace('srpna','8.').replace('září','9.').replace('října','10.').replace('listopadu','11.').replace('prosince','12.').replace(' ','')
            if (re.search(r"Spoj\s\d{2}:", radek)) or ('html>' in radek):
                if spoj:
                    spoje.append(spoj)
            if (re.search(r"Spoj\s\d{2}:", radek)):
                spoj = {}
                spoj['prodejce'] = "RJ"
                spoj['odkud'], spoj['kam'] = soubor.split('_')[1], soubor.split('_')[2]
                odjezdprijezd = radek.replace('+1','').split('>')[-1].split(' - ')
                oscrapovano = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', soubor).group(0)
                spoj['oscrapovano'] = datetime.strptime(oscrapovano, "%Y-%m-%d_%H-%M-%S")
                spoj['odjezd'] = datetime.strptime('-'.join(datum.split('-')[::-1]) + " " + odjezdprijezd[0].strip(), "%d.%m.%Y %H:%M")
                spoj['predstih'] = spoj['odjezd'] - spoj['oscrapovano']
                spoj['den'] = den
            if "Délka cesty" in radek:
                if spoj:
                    jizdni_doba = re.search(r"\d\d:\d\d",radek).group(0)
                    jizdni_doba = [int(x) for x in jizdni_doba.split(':')]
                    spoj['jizdni_doba'] = jizdni_doba[0] * 60 + jizdni_doba[1]
            if re.search(r"\d{1,5}&nbsp;Kč",radek):
                if spoj:
                    cena = re.search(r"\d{1,5}Kč", radek.replace(" ","").replace("&nbsp;","")).group(0)
                    spoj['cena'] = int(cena.split("Kč")[0])
                    if spoj['cena'] == 79:
                        print(radek)
            if "Volných míst" in radek:
                if spoj:
                    spoj['volnych_mist'] = int(re.search(r"\d{1,6}", radek).group(0))
            if "Vyprodáno" in radek:
                if spoj:
                    spoj['volnych_mist'] = 0
            if "přestup" in radek:
                prestupy = re.search(r'>\d',radek)
                if prestupy != None:
                    spoj['prestupy'] = int(prestupy.group(0)[1])
            if ">Přímý" in radek:
                spoj['prestupy'] = 0
            if "M5 17.526c0 .788.341 1.494.875 1.987v1.145c0 .742.586 1.342 1.313 1.342.726 0 1.312-.6 1.312-1.342v-.448h7v.448c0 .734.586 1.342 1.313 1.342.717 0 1.312-.6 1.312-1.342v-1.145A2.698 2.698 0 0 0 19 17.526V8.58C19 5.447 15.867 5 12 5s-7 .447-7 3.579v8.947Zm3.063.895c-.727 0-1.313-.6-1.313-1.342 0-.743.586-1.342 1.313-1.342.726 0 1.312.6 1.312 1.342 0 .743-.586 1.342-1.313 1.342Zm7.874 0c-.726 0-1.312-.6-1.312-1.342 0-.743.586-1.342 1.313-1.342.726 0 1.312.6 1.312 1.342 0 .743-.586 1.342-1.313 1.342Zm1.313-5.368H6.75V8.579h10.5v4.474Z" in radek:
                if spoj != None:
                    spoj['prostredek'] = 'autobus'
            if "M7 2h10v1.5h-3.204l-.772 1.515C16.151 5.113 19 5.754 19 8.579v8.5c0 1.727-1.374 3.131-3.063 3.131l.998 1.03c.28.277.088.76-.306.76h-.954a.44.44 0 0 1-.306-.134L13.75 20.21h-3.5l-1.619 1.655a.406.406 0 0 1-.306.134h-.954c-.394 0-.586-.483-.315-.76l1.006-1.03C6.375 20.21 5 18.806 5 17.08v-8.5c0-2.834 2.866-3.47 6.004-3.565l.772-1.514H7V2Zm-.25 15.079c0 .743.586 1.342 1.313 1.342.726 0 1.312-.6 1.312-1.342 0-.743-.586-1.342-1.313-1.342-.726 0-1.312.6-1.312 1.342Zm0-4.921h4.375V8.579H6.75v3.579Zm7.875 4.92c0 .744.586 1.343 1.313 1.343.726 0 1.312-.6 1.312-1.342 0-.743-.586-1.342-1.313-1.342-.726 0-1.312.6-1.312 1.342Zm-1.75-4.92h4.375V8.579h-4.375v3.579Z" in radek:
                if spoj != None:
                    spoj['prostredek'] = 'vlak'
    return [x for x in spoje if x != None]


# In[3]:


kam = "data" 
os.makedirs(kam, exist_ok=True)
hotove = [y for y in os.listdir(kam) if y[0:3] == "rj_"] 
hotove = hotove # [:-1]
# hotove = []
for x in os.listdir("downloads"):
    nazev_souboru = "rj_" + x + ".parquet"
    if nazev_souboru not in hotove:
        den = []
        rj = [y for y in os.listdir(f"downloads/{x}") if y[0:3] == "rj_"] 
        print(f"{x}: {len(rj)}")
        for y in rj:
            den = den + oscrapuj_rj(f"downloads/{x}",y)  
        if len(den) > 5:
            df_den = pd.DataFrame(den)
            df_den.to_parquet(os.path.join(kam,nazev_souboru))

