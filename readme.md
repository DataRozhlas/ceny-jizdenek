Skripty sbírají data z webů vlakových dopravců (ČD, RegioJet, Arriva, Leo Express). S pomocí těchto dat zde zjišťujeme, jak se v závislosti na čase nákupu a jiných okolnostech mění ceny jízdenek, kdy jezdí vlaky nejplnější atd.

Update 2025-06-03:

Kvůli velikosti dat (přes 8 milionů jízdenek) jsem musel 1/ přejít při čištění z pandas na Polars, 2/ rozsekat monolitický soubor ```jizdenky.parquet``` na čtyři menší soubory po jednotlivých dopravcích. (Ty ještě čeká mírná optimalizace, některé sloupce se u nich liší.) Všechna data zůstala, ale je možné, že se někde po změně čištího nástroje stala drobná chyba např. v datatypu, jejíž následky v tuto chvíli nedohlédnu.

Použití:

- Soubory ```data/jizdenkyDOPRAVCE.parquet``` obsahují téměř kompletní posbíraná data. Pozor, data mají limity. Doba mezi uložením ceny jízdenky a odjezdem vlaku je do jisté míry předurčená a se zároveň se mezi jednotlivými spoji liší. Z dat tedy nelze detailně vyčíst postup zaplňování vlaků nebo růst cen bezprostředně před odjezdem. Různí dopravci informují o dostupných místech různými způsoby: České dráhy slovním popisem obsazenosti, RegioJet přesným počtem volných míst, Leo Express přesným počtem, jen pokud je míst k dispozici méně než dvacet – je tedy obtížné vyčíslit zaplněnost jednotným způsobem. Do cen budoucích spojů se ve sledovaném období promítají prosincové změny jízdních řádů i cen jízdného. Data neobsahují (a článek proto nesrovnává) informace o službách zahrnutých v ceně jízdenky, ani o typických zpožděních či četnosti rušení vagónů nebo celých spojů. Dopravci nabízejí různé věrnostní slevy. Lišit se mohou i storno podmínky, zvlášť u mezistátních vlaků. Některé mezistátní jízdenky může být výhodnější nakoupit u zahraničního dopravce. Toto vše je nutné mít při analýze na paměti.

- Sešity a skripty od č. 000 do č. 099 stahují, scrapují a čistí data. Sešity od č. 100 jsou věnované exploraci, může v nich být mnoho omylů a nepřesností. Sešity od č. 900 jsou finálními zdroji pro články na iROZHLAS.cz.

To-do programovací:

- U některých zahraničních spojů potřebuje doladit scrapování Českých drah – jde o ty, kde je nutné se během cesty přesunout pěšky mezi nádražími. Pro účely článků doposud publikovaných na iROZHLAS.cz je to vcelku jedno (do statistik se nepropíšou některé obskurnější spoje), nicméně to při dalším bádání může být matoucí, protože z takových spojů se do čistých dat uloží jen druhá část za přesunem (např. Berlín-Amsterdam).

- Nějak vypadlo mnoho spojů RJ (zdaleka ne všechny), což bude na větší inspekci.

- Přidat OneTicket.

To-do badatelské:

- „Když se koupí na stejný vlak a stejné místo na vlak Praha - Budapešť, tak v aplikaci maďarských drah zaplatí člověk často půlku toho co u Českých drah, které vlak provozují.“ (Tip z FB.)

- Jízdenky pro psy. (Tip od JC.)

Note to self: rozběhnout Selenium na Raspberry Pi mi pomohly tyto návody:

- [https://nicolaslouge.com/post/how-to-set-up-selenium-python-geckodriver-raspberry-pi-arm-2023/](https://nicolaslouge.com/post/how-to-set-up-selenium-python-geckodriver-raspberry-pi-arm-2023/)
- [https://patrikmojzis.medium.com/how-to-run-selenium-using-python-on-raspberry-pi-d3fe058f011](https://patrikmojzis.medium.com/how-to-run-selenium-using-python-on-raspberry-pi-d3fe058f011)
- [https://stackoverflow.com/questions/64979042/how-to-run-seleniumchrome-on-raspberry-pi-4](https://stackoverflow.com/questions/64979042/how-to-run-seleniumchrome-on-raspberry-pi-4)