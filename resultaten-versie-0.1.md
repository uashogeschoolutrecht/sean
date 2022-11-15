# Sean the HU sentimenent analysis algorithm 
> 
    Versie        : sean 0.01
    Auteurs       : Anne Leemans/Fraukje Coopmans
    Start datum   : 27/10/2022

![](images/Sean_branding.png)

### Wat is het?
De insteek van dit project is om algemene modellen te ontwikkelen die breed inzetbaar zijn en als off-the-shelf data-science producten gebruikt kunnen worden. Het uiteindelijke doel van het project is om een omgeving in te richten waar medewerkers deze off-the-shelf data-science producten kunnen afnemen. In brede zin kan gedacht worden aan een interactieve omgeving die Python (of R) projecten aanstuurt (eventueel na input van de gebruiker).
<br></br>
### Wat hebben we?
Voor de start van dit project zijn we allereerst begonnen met het opzetten van een data-science tool alvorens we ons gaan buigen over het inrichten van de omgeving. Daarbij hebben we ons gericht op een sentiment analyse op Topdesk-meldingen. 
<br></br>
### Topdesk-meldingen
Bij de analyse hebben we gekeken naar verzoeken die via de mail binnen zijn gekomen. Deze hebben we via een directe link uit het datawarehouse in python geladen. De verzoeken die in het datawarehouse opgeslagen zijn bevattend de gehele mail.  Voordat we hier een sentiment analyse op los konden laten hebben we deze eerst moeten schonen. Omdat de gehele als één stuk tekst opgeslagen is was de eerste stap om de afzonderlijk mails te identificeren.  


```ruby
# Aantal email in de verzoek kolom tellen
df['onderwerp_count'] = df[colum].str.count(r'(Onderwerp:|Subject:)')

# Kijken wat het maximaal aantal mails is
split_len = max(df['onderwerp_count'])

# Aantal kolommen uitbreiden met max aantal keer dat mails voorkomt
cols = list()
for i in range(split_len+1):
    cols += ['onderwerp_{}'.format(i)]

# Per mail een aparte onderwerp kolom maken en daar de resultaten van de split in zetten
df[cols] = df[colum].str.split('Onderwerp:.*?\n', expand=True)
```

Bij de sentiment analyse hebben we alleen naar het initiële verzoek gekeken. Dus na de split hebben we alleen het eerste mail behouden en de rest weggegooid. Vervolgens hebben we deze mail verder opgeschoond door alle niet relevantie informatie weg te laten.


```ruby
def schoonmaken(df, col):

    '''Deze functie schoont e-mails op door zoveel mogelijk overbodige tekst weg te halen'''
    
    # Kolommen omzetten naar string
    df[col] = df[col].astype(str)

    # Het gaat hier om email berichten, veel voorkomende niks zeggende info kan weggelaten worden.
    df[col] = df[col].str.replace(r'(Geachte.{1,30}\n|Goedemiddag.{1,30}\n|Goedeavond.{1,30}\n|Beste.{1,20}\n)',' ')

    # Alle line-breaks omzetten naar ###-
    df[col] = df[col].str.replace(r'\n',' ### ')
    df[col] = df[col].str.replace(r'(vriendelijke groet.*|mvg.*|kind regards.*)','')
    df[col] = df[col].str.replace(r'van:.*?verzonden:.*?aan:.*','')

    # Alle ### weer terugzetten naar line breaks
    df[col] = df[col].str.replace(r' ### ','\n')

    # Alles omzetten naar kleine letters
    df[col] = df[col].str.lower()

    # Alles wat niet tekstueel is weglaten
    df[col] = df[col].str.replace('[^A-záéíóúýçäëïöüÿàèìòùâêîôûãõñ]', ' ')
```
Tot slot wordt nog de taal van de teksten geidentifficeerd, in deze eerste versie kijken we alleen naar Nederlandse reviews

```ruby
# Taal detecter om te bepalen welk woordenboek gebruikt moet worden
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0

    df['taal'] = df['onderwerp_1'].apply(lambda x: detect(x))
```
Nu de mails geïdentificeerd en geschoond zijn kunnen we de sentiment analyse erop loslaten.
<br></br>
## Sentiment analyse
Sentiment analyse scoort korte stukken tekst op basis van de woorden of combinatie van woorden. Doel is om te achterhalen of de tekst een positieve of negatieve connotatie heeft. Aan de hand van handmatig geclassificeerde stukken tekst kan een model ontwikkeld worden dat in staat is om deze scores toe te wijzen.
<br></br>
### Twee modellen
Bij de eerste versie van dit project hebben we gebruik gemaakt van twee verschillende modellen:
1.  [Dutch RoBERTa-based Language Model](https://arxiv.org/pdf/2001.06286.pdf) dit model maakt gebruikt van een ***boolean*** methode waarbij stukken tekst enkel als ***positief*** of ***negatief*** geclassificeerd worden (dus geen neutraal optie). Ook wordt er een betrouwbaarheidsscore toegewezen die loopt van ***0,5*** tot ***1***. Het gebruikte model is getraind op basis van een review dataset DBRD. Dit is een dataset die bestaat uit 118.516 boek reviews die vervolgens door gebruikers gescoord zijn. Voor het trainen van RoBERTa zijn 22.252 van deze reviews gebruikt. Dit model hebben we vervolgens zelf getest door te kijken naar hotel reviews van een aantal hotels in Maastricht die we met een webscraper van [Tripadvisor.nl]('https://www.tripadvisor.nl/) gescraped hebben. Uit deze test bleek dat het model voor 90% betrouwbaar was. Hierbij moet wel opgemerkt worden dat het model getraind is op reviews (van boeken) en het is dus maar de vraag hoe goed dit op andere bronnen toepasbaar is. Het voordeel is wel dat dit model specifiek voor Nederlandstalige teksten is ontwikkeld. 
2.  [Bert multilingual sentiment](https://arxiv.org/pdf/2007.13061.pdf) dit model maakt gebruik van een 5punts ***likert scale*** die loopt van heel negatief naar heel positief. Elk stuk tekst krijgt per punt op deze schaal een score tussen ***0.0*** en ***1.0***. Waarbij het totaal altijd 1 is, een stuk tekst kan bijv. 0,9 positief en 0,1 heel positief zijn. Deze data is getraind op Wikipedia-data dumps van 104 talen. Het model is niet getest op de review data van Tripadvisor. In een volgende versie is dit wel een gewenste toevoeging. 
   
>   Beide modellen kunnen [hier](https://huggingface.co/models?language=nl&sort=downloads&search=sentiment) gevonden worden.

## Resultaten 
In de onderstaande figuur staan de resultaten van beide modellen. Er is een uitsplitsing gemaakt naar een aantal onderwerpen, daarbij is steeds naar de 15 meest voorkomende onderwerpen gekeken. Bij de analyse met het boolean model zijn alleen resulaten meegenomen met een betrouwbaarheid van > 0.95.

![image.png](/python-scripts/images/side-by-side.png)

De resultaten laten zien dat gemiddeld genomen de e-mails overwegend negatief zijn, alleen de onderwerpen ***waarmerken documenten, formulieren, inschrijven en inhoudelijke vragen onderwijs*** laten een positief sentiment zien. 

Als we kijken naar de verschillen tussen de twee modellen lijken die vergelijkbaar te zijn. 

De getoonde resultaten zeggen echter niks over de betrouwbaarheid van de analyse. Een korte scan op de teksten laat zien dat een handmatige classificatie de e-mails eerder in een neutrale categorie vallen en niet direct positief of negatief zijn. 
<br></br>
### Stappen ter verbetering sentiment
Op basis van de huidige analyse is moeilijk in te schatten of de sentiment analyse betrouwbare resultaten oplevert. Een eerste stap om dit te verbeteren zou zijn om een sample van de e-mails handmatig te scoren en deze resultaten vervolgens naast de resultaten van het algoritme leggen. 
Om vervolgens de betrouwbaarheid nog verder te vergoten kan in eerste instantie nog meer winst gehaald worden in het beter schonen van de analyse teksten (e-mails). Het beste resultaat wordt echter gehaald door zeer grote sample handmatig classificeren en die als trainingset gebruiken om zelf een model te maken. Dit is vermoedelijk te tijdsintensief, een andere oplossing kan zijn om andere (betere) voorgetrainde modellen te gebruiken. 

