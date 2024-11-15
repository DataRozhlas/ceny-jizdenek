Skripty sbírají data z webů vlakových dopravců (ČD, RegioJet, Arriva, Leo Express). S pomocí těchto dat zde posléze zjistíme, jak se v závislosti na čase nákupu a jiných okolnostech mění ceny jízdenek, kdy jezdí vlaky nejplnější atd.

Použití:

- Soubor ```data/jizdenky.parquet``` obsahuje téměř kompletní posbíraná data. Pozor při jejich interpretaci! Jsou postahovaná v předem určených časech a na předem určených trasách (sledujeme především přepravu mezi velkými městy), nezahrnují ani základní slevy, jednotliví dopravci mají různé metriky obsazenosti (slovní popis, přesná cifra, přesná cifra pod 20 volných míst), občas se tam zamíchá jiná trasa než hledaná atd. Navíc se ve sledovaném časovém okně (sběr dat začal v listopadu 2024 a pokračuje do začátku roku 2025) mění jízdní řady a s ním i ceny.
- Soubor ```data/jizdenky_tyden.csv``` filtruje spojení oscrapovaná v posledních 168 hodinách (ve smyslu před ruční aktualizací dat a repozitáře) pro rychlejší a jednodušší exploraci. Výše uvedené vykřičníky platí i zde.

To-do programovací:

- Průběžně scrapovat stažené stránky a mazat originály (jsou mega velké).
- Přidat OneTicket.

To-do badatelské:

- „Když se koupí na stejný vlak a stejné místo na vlak Praha - Budapešť, tak v aplikaci maďarských drah zaplatí člověk často půlku toho co u Českých drah, které vlak provozují.“ (Tip z FB.)
- Jízdenky pro psy. (Tip od JC.)

Note to self: rozběhnout Selenium na Raspberry Pi mi pomohly tyto návody:

- [https://nicolaslouge.com/post/how-to-set-up-selenium-python-geckodriver-raspberry-pi-arm-2023/](https://nicolaslouge.com/post/how-to-set-up-selenium-python-geckodriver-raspberry-pi-arm-2023/)
- [https://patrikmojzis.medium.com/how-to-run-selenium-using-python-on-raspberry-pi-d3fe058f011](https://patrikmojzis.medium.com/how-to-run-selenium-using-python-on-raspberry-pi-d3fe058f011)
- [https://stackoverflow.com/questions/64979042/how-to-run-seleniumchrome-on-raspberry-pi-4](https://stackoverflow.com/questions/64979042/how-to-run-seleniumchrome-on-raspberry-pi-4)