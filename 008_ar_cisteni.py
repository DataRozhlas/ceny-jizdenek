#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
from datetime import datetime
import pandas as pd


# In[2]:


def oscrapuj_ar(slozka, soubor):
    with open(os.path.join(slozka,soubor), "r", encoding="utf-8") as spojeni:
        spojeni = spojeni.read()
        spoje = []
        spoj = None
        oscrapovano = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', soubor).group(0)
        oscrapovano = datetime.strptime(oscrapovano, "%Y-%m-%d_%H-%M-%S")
        for index, radek in enumerate(spojeni.split(">")):
            if len(radek) < 1000:
                if re.search(r"\d{1,2}\.\s\w{4,15}\s20\d{2}", radek):
                    datum = re.search(r"\d{1,2}\.\s\w{4,15}\s20\d{2}", radek).group(0)
                    datum = datum.replace("leden","1.").replace("únor","2.").replace("březen","3.").replace("duben","4.").replace("květen","5.").replace("červen","6.").replace('červenec','7.').replace('srpen','8.').replace('září','9.').replace('říjen','10.').replace('listopad','11.').replace('prosinec','12.').replace(' ','')
                elif ('class="departure"' in radek) or ('</html' in radek):
                    if spoj:
                        spoj['prestupy'] = len(spoj['vlaky']) - 1
                        spoje.append(spoj)
                    spoj = {}
                    spoj['vlaky'] = []
                    spoj['prodejce'] = 'ARR'
                    spoj['prostredek'] = 'vlak'
                    spoj['odkud'] = spojeni.split(">")[index + 1].split("<")[0]
                    spoj['oscrapovano'] = oscrapovano
                elif '<div class="arrival"' in radek:
                    spoj['kam'] = spojeni.split(">")[index + 1].split("<")[0]
                elif '<div class="time"' in radek:
                    cas = spojeni.split(">")[index + 2].split("<")[0]
                    try:
                        spoj['odjezd'] = datetime.strptime('.'.join(datum.split('.')) + " " + cas.strip(), "%d.%m.%Y %H:%M")
                        spoj['predstih'] = spoj['odjezd'] - oscrapovano
                    except:
                        spoj['odjezd'] = None
                        print("UWAGA UWAGA, nepodařilo se najít čas odjezdu.")
                elif 'Vzdálenost' in radek:
                    spoj['vzdalenost'] = int(re.search(r"\d{1,4}",radek).group())
                elif ("hodin" in radek) and ("minut" in radek):
                    jizdni_doba = radek.split(' a ')
                    hodiny = re.search(r"\d{1,2}", jizdni_doba[0]).group()
                    minuty = re.search(r"\d{1,2}", jizdni_doba[1]).group()
                    spoj['jizdni_doba'] = (int(hodiny) * 60) + int(minuty)
                elif "&nbsp;Kč" in radek:
                    spoj['cena'] = int(re.search(r"\d{1,5}", radek.split("&nbsp;Kč")[0]).group())
                elif 'class="line-number" ' in radek:
                    spoj['vlaky'].append(spojeni.split(">")[index + 1].split("<")[0])
                elif '<span class="priceFreeSeats"' in radek:
                    spoj['volnych_mist'] = int(re.search(r'\d{1,4}', spojeni.split(">")[index + 1]).group())
    return [x for x in spoje if x != None]


# In[3]:


kam = "data" 
os.makedirs(kam, exist_ok=True)
hotove = [y for y in os.listdir(kam) if y[0:3] == "ar_"]
hotove = hotove
# hotove = []
for x in os.listdir("downloads"):
    nazev_souboru = "ar_" + x + ".parquet"
    if nazev_souboru not in hotove:
        den = []
        ar = [y for y in os.listdir(f"downloads/{x}") if y[0:3] == "ar_"] 
        print(f"{x}: {len(ar)}")
        for y in ar:
            den = den + oscrapuj_ar(f"downloads/{x}",y)
        if len(den) > 0:
            df_den = pd.DataFrame(den)
            df_den.to_parquet(os.path.join(kam,nazev_souboru))


# In[ ]:




