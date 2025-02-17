#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
from datetime import datetime
import pandas as pd


# In[2]:


def oscrapuj_le(slozka, soubor):

    def mista(i):
        return int(spojeni.split(">")[index + 2].split('<')[0].strip().replace('&gt; 20','21'))
    
    with open(os.path.join(slozka,soubor), "r", encoding="utf-8") as spojeni:
        spojeni = spojeni.read()
    spoje = []
    spoj = None
    pocitadlo_casu = 1
    oscrapovano = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', soubor).group(0)
    oscrapovano = datetime.strptime(oscrapovano, "%Y-%m-%d_%H-%M-%S")
    for index, radek in enumerate(spojeni.split(">")):
        if len(radek) < 1000:
            format_data = r"\w{4,10}, \d{2}\. \d{2}\. 202\d"
            if re.search(format_data, radek):
                datum = re.search(format_data, radek).group(0)
                den = datum.split(',')[0].strip().lower()
                datum = datum.split(',')[1].strip().replace(' ','')
            elif (re.search(r"\d{2}:\d{2}", radek[0:5])):
                pocitadlo_casu += 1
                if pocitadlo_casu % 2 == 0:
                    if spoj:
                        if spoj != None:
                            spoj['oscrapovano'] = oscrapovano
                            spoj['predstih'] = spoj['odjezd'] - oscrapovano
                            spoj['prodejce'] = 'LE'
                            spoj['vlaky'] = set(spoj['vlaky'])
                            spoj['prestupy'] = len(spoj['vlaky']) - 1
                            try:
                                spoj['volnych_mist'] = spoj['volna_mista_economy'] + spoj['volna_mista_economy_plus'] + spoj['volna_mista_economy_business'] + spoj['volna_mista_premium']
                            except:
                                pass
                            spoje.append(spoj)
                    spoj = {}
                    spoj['vlaky'] = []
                    spoj['odkud'] = None
                    cas = radek[0:5]
                    spoj['odjezd'] = datetime.strptime('.'.join(datum.split('.')) + " " + cas.strip(), "%d.%m.%Y %H:%M")
            elif '</html' in radek:
                if spoj:
                    if spoj != None:
                        spoj['oscrapovano'] = oscrapovano
                        spoj['predstih'] = spoj['odjezd'] - oscrapovano
                        spoj['prodejce'] = 'LE'
                        spoj['vlaky'] = set(spoj['vlaky'])
                        spoj['prestupy'] = len(spoj['vlaky']) - 1
                        try:
                            spoj['volnych_mist'] = spoj['volna_mista_economy'] + spoj['volna_mista_economy_plus'] + spoj['volna_mista_economy_business'] + spoj['volna_mista_premium']
                        except:
                            pass
                        spoje.append(spoj)
            elif ("Ostrava" in radek[0:10]) or ("Praha" in radek[0:10]) or ("Pardubi" in radek[0:10]) or ("Kraków" in radek[0:10]) or ("Košice" in radek[0:10]):
                if spoj != None:
                    if spoj['odkud'] == None:
                        spoj['odkud'] = radek.split("<")[0].strip()
                    else:
                        spoj['kam'] = radek.split("<")[0].strip()            
            elif "&nbsp;Kč" in radek:
                spoj['cena'] = re.search(r'\d{1,5}', radek.replace("&nbsp;","").split('|')[-1]).group()
            elif " km<" in radek:
                spoj['vzdalenost'] = int(re.search(r'\d{1,5}', radek).group(0))
            elif re.search(r'\d{1,2} h \d{1,2} min', radek):
                jizdni_doba = radek.split('|')[0]
                jizdni_doba = jizdni_doba.split('h')
                h = re.search(r"\d{1,2}", jizdni_doba[0]).group()
                min = re.search(r"\d{1,2}", jizdni_doba[1]).group()
                spoj['jizdni_doba'] = (int(h) * 60) + int(min)
            elif "Economy<" in radek[0:10]:
                spoj['volna_mista_economy'] = mista(index) # spojeni.split(">")[index + 2].split('<')[0].strip()
            elif "Economy P" in radek[0:10]:
                spoj['volna_mista_economy_plus'] = mista(index) # spojeni.split(">")[index + 2].split('<')[0].strip()
            elif "Business" in radek[0:10]:
                spoj['volna_mista_economy_business'] = mista(index) # spojeni.split(">")[index + 2].split('<')[0].strip()
            elif "Premium<" in radek[0:10]:
                spoj['volna_mista_premium'] = mista(index) # spojeni.split(">")[index + 2].split('<')[0].strip()
            elif re.search(r"LE\d{2}", radek[0:4]):
                spoj['vlaky'].append(re.search(r"LE\d{1,7}", radek).group())
    return [x for x in spoje if x != None]


# In[3]:


kam = "data" 
os.makedirs(kam, exist_ok=True)
hotove = [y for y in os.listdir(kam) if y[0:3] == "le_"] 
hotove = hotove
# hotove = []
for x in os.listdir("downloads"):
    nazev_souboru = "le_" + x + ".parquet"
    if nazev_souboru not in hotove:
        den = []
        le = [y for y in os.listdir(f"downloads/{x}") if y[0:3] == "le_"] 
        if len(le) > 0:
            print(f"{x}: {len(le)}")
            for y in le:
                den = den + oscrapuj_le(f"downloads/{x}",y)
        if len(den) > 0:
            df_den = pd.DataFrame(den)
            df_den.to_parquet(os.path.join(kam,nazev_souboru))

