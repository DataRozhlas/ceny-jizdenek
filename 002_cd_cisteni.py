#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
from datetime import datetime
import pandas as pd


# In[2]:


def oscrapuj_cd(slozka, soubor):
    
    with open(os.path.join(slozka, soubor), "r", encoding="utf-8") as file:
        raw_html = file.read()

    oscrapovano = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', soubor).group(0)
    
    spojeni = raw_html.split("""<article""")
    spojeni = spojeni[1:]
    slovniky = []
    for s in spojeni:
        s = s.splitlines()
        slovnik = {}
        slovnik['prodejce'] = "ČD"
        slovnik['vlaky'], slovnik['obsazenost'], slovnik['zpozdeni'] = [], [], []
        slovnik['oscrapovano'] = datetime.strptime(oscrapovano, "%Y-%m-%d_%H-%M-%S")
        den = False
        for radek in s:
            if len(radek) < 500:
                if "text: to(lastTrain($index()))" in radek:
                    slovnik['kam'] = radek.split('>')[-2].split('<')[0]
                elif "text: from(firstTrain($index()))" in radek:
                    slovnik['odkud'] = radek.split('>')[-2].split('<')[0]
                elif ("text: journeyDateTextFrom()" in radek) and (den == False):
                    den = radek.split('>')[-2].split('<')[0]
                elif "text: depTime(firstTrain($index()))" in radek:
                    cas_odjezdu = re.search(r"\d{1,2}:\d\d", radek).group(0)
                elif "text: buyButtonText()" in radek:
                    cena = radek.split('-->')[1].split('<!--')[0].replace(" Kč","")
                    try:
                        slovnik['cena'] = int(cena)
                    except:
                        pass
                elif "Zjistit cenu" in radek:
                    slovnik['cena_poznamka'] = "Zjistit cenu"
                elif "Cena v dalším kroku" in radek:
                    slovnik['cena_poznamka'] = "Cena v dalším kroku"
                elif "text: model.trainTypeAndNum" in radek:
                    if radek.split('-->')[1].split('<!--')[0] not in slovnik['vlaky']:
                        slovnik['vlaky'].append(radek.split('-->')[1].split('<!--')[0])
                elif """<span aria-hidden="true" data-bind="visible: occupancyLevelFull(), text: occupancyLevelText()" style="display: none;">""" in radek:
                    slovnik['obsazenost'].append(radek.split('>')[-2].split('<')[0])
                elif """<span data-bind="text: timeLength, visible: timeLength != null &amp;&amp; timeLength != ''">""" in radek:
                    jizdni_doba = radek.split('>')[-2].split('<')[0].split(":")
                    slovnik['jizdni_doba'] = (int(jizdni_doba[0]) * 60) + int(re.search(r'\d\d', jizdni_doba[1]).group(0))
                elif """<span data-bind="text: distance, visible: distance != null &amp;&amp; distance != ''" class="mobile-hidden">""" in radek:
                    vzdalenost = radek.split('>')[-2].split('<')[0].replace(" km","")
                    try:
                        slovnik['vzdalenost'] = int(vzdalenost)
                    except:
                        pass
                elif """<span class="icon icon-bus" data-bind="ifnot: isLegend, visible: !isLegend &amp;&amp; icoSrc, css: icoSrc, attr: {title: desc, 'aria-label': desc}" title="Náhradní autobusová doprava" aria-label="Náhradní autobusová doprava"></span>""" in radek:
                    slovnik['nahradni_bus'] = True
                elif """<span aria-hidden="true" data-bind="text: delayText()">""" in radek:
                    if "+" in radek:
                        try:
                            slovnik['zpozdeni'].append(int(radek.split('+')[1].strip().split(' ')[0]))
                        except:
                            slovnik['zpozdeni'].append('chyba')
                    elif "><" in radek:
                        slovnik['zpozdeni'].append(0)
                elif "Místenka zdarma" in radek:
                    slovnik['mistenka_zdarma'] = True
        slovnik['den'] = den.split(' ')[0].lower().strip()
        slovnik['odjezd'] = datetime.strptime('-'.join(den.split(' ')[1].split('.')[::-1]) + " " + cas_odjezdu, "%Y-%m-%d %H:%M")
        slovnik['predstih'] = slovnik['odjezd'] - slovnik['oscrapovano']
        if len(slovnik['vlaky']) == 1:
            slovnik['vlaky'] = [slovnik['vlaky'][0]]
            try:
                slovnik['obsazenost'] = [slovnik['obsazenost'][0]] ## todo: obsazenost se přidává n+1×, toto je laciný workaround pro většinu případů 
            except:
                pass
        slovnik['zpozdeni'] = slovnik['zpozdeni'][1::2]
        slovnik['prestupy'] = len(slovnik['vlaky']) - 1
        slovnik['prostredek'] = 'vlak'
        slovniky.append(slovnik)
    return [x for x in slovniky if x != None]


# In[3]:


kam = "data" 
os.makedirs(kam, exist_ok=True)
hotove = [y for y in os.listdir(kam) if y[0:3] == "cd_"]
hotove = hotove
# hotove = []
for x in os.listdir("downloads"):
    nazev_souboru = "cd_" + x + ".parquet"
    if nazev_souboru not in hotove:
        print(nazev_souboru)
        den = []
        cd = [y for y in os.listdir(f"downloads/{x}") if "cd_" in y] 
        print(f"{x}: {len(cd)}")
        for y in cd:
            den = den + oscrapuj_cd(f"downloads/{x}",y)
        df_den = pd.DataFrame(den).sort_values(by="oscrapovano").reset_index(drop=True)
        df_den.to_parquet(os.path.join(kam,nazev_souboru))

