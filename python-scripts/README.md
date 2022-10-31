# SEAN

- Author: Anne Leemans
- Date: 27/10/2022
- Hogeschool Utrecht


## Requirements
- Chromdriver kan [hier](https://chromedriver.chromium.org/downloads) gedownload worden. Sla deze op in de hoofdmap van deze repo. 
- Laatste ODBC driver kan [hier](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) gedownload worden.

> **_LET OP!:_** check de versie van je chrome en zorg dat deze overeenkomt met de chrome driver
> 
##  About

Sean is een algoritme dat vrije tekst kan lezen en een classificatie kan toepassen op basis van het aanwezige sentiment. Het doel is een HU product te ontwikkelen (bijv. R package) dat vrij beschikbaar is ten behoeve van sentiment analyse, dit kan bijvoorbeeld via GitHub geborgd en beheerd worden. 


Sean profileert zich als een D&A/DDHU off the shelve data science product. Insteek is algemeen model (algoritme) ontwikkelen, wat breed inzetbaar is (bijv. Topdesk meldingen, open vragen vragenlijsten, voeden van andere modellen). Pipeline met hoe het algoritme interacteert met HU DWH moet nog uitgedacht worden, wellicht een directe koppeling R <-> HU DWH. Of en hoe deze self-service ingezet zou kunnen worden moet nog uitgedacht worden. 

Sentiment kan op lage granulariteit (persoon-bericht/vraag) berekend kunnen worden, en is daardoor aggregeerbaar naar hogere granulariteit (alle vragen/OE/instituut/behandelaarsgroep/periode/etc.). 

## Kennishouders sentiment analyse
- Externe partij Totta (ingehuurd door M&C)
- Anne Leemans
- Jaap Semeijn
- Philippine Waisvisz
- Marc Teunis (?)
- Marie Corradi (?)
- Fraukje Coopmans

## Toepassingen
Veerle vertelt dat er nú al een pilot loopt (gefinancierd vanuit M&C met externe partij Totta) op voice waarbij sentiment en effort wordt bepaald. Andere toepassingen zijn: open vragen vragen met veel respondenten (NSE, 100 dagen, SKC, etc.), Topdesk meldingen, mogelijk ook HU Twitter, ... 
Joan heeft sentiment analyse toegepast op open vragen Exit monitor, maar hier was het aantal data van zo'n kleine hoeveelheid dat de opleidingsmanagers aangaven geen toegevoegde waarde te zien op text analyse: ze kunnen namelijk net zo makkelijk zelf door alle open antwoorden heen lezen. 
Christine ziet nog niet direct meerwaarde bij toepassing op NSE open vragen. 

## Effort
Tijdsinvestering is eenmalig medium (~1-3 maanden) en zit vooral in het opzetten/vinden van een woordenboek en trainen van algoritme. Na eerste versie algoritme is de tijdsinvestering laag (doorontwikkeling, verbetering). 

## Tooling
Nog te bepalen: R of Python
Ontwikkeling via git en HU GitHub zodat HU-brede toegang en doorontwikkeling van het algoritme laagdrempelig mogelijk is. 

## Complexiteit/risico's
Beschikbare data heeft veel data-wrangling nodig.
Toepassing op open vragenlijst vragen heeft mogelijk weinig draagvlake

## literatuur en links
- [SoNaR-Corpus](https://taalmaterialen.ivdnt.org/download/tstc-sonar-corpus/)
- [Dutch RoBERTa-based Language Model](https://arxiv.org/pdf/2001.06286.pdf)
- [Bert](https://arxiv.org/pdf/1810.04805.pdf&usg=ALkJrhhzxlCL6yTht2BRmH9atgvKFxHsxQ)
- [Training set](https://huggingface.co/DTAI-KULeuven/robbert-v2-dutch-sentiment?text=Ik+erken+dat+dit+een+boek+is%2C+daarmee+is+alles+gezegd.)
- [Trianing script](https://github.com/benjaminvdb/DBRD)