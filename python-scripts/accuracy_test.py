########
'''Model testen op basis van reviews op tripadivsor'''

# model instellen
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import pipeline
model_name = 'DTAI-KULeuven/robbert-v2-dutch-sentiment' # voor meer info https://huggingface.co/DTAI-KULeuven/robbert-v2-dutch-sentiment?text=Ik+erken+dat+dit+een+boek+is%2C+daarmee+is+alles+gezegd.
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

# classifier instellen
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

from scraper.tripadvisorscraper import hotelScraper

# vul een hotel url in
url = 'https://www.tripadvisor.nl/Hotel_Review-g188575-d230890-Reviews-Amrath_Grand_Hotel_de_l_Empereur-Maastricht_Limburg_Province.html#REVIEWS'

df = hotelScraper(url)

df.reset_index(drop=True, inplace=True)

# alle lege reviews weglaten
df = df[~df['review'].isnull()]
df['accuraatheid'] = 0
df['sentiment'] = ''

# sentiment check
for i in df.index:
    temp = classifier(df['review'][i])
    df['sentiment'][i] = temp[0]['label']
    df['accuraatheid'][i] = temp[0]['score']


df['review_clean'] = df['review']

# schoonmaken
from other.cleaning import schoonmaken
df = schoonmaken(df=df,col='review_clean')

df['accuraatheid_cl'] = 0
df['sentiment_cl'] = ''

# sentiment check
for i in df.index:
    temp = classifier(df['review_clean'][i])
    df['sentiment_cl'][i] = temp[0]['label']
    df['accuraatheid_cl'][i] = temp[0]['score']

# backupbestand maken
backup = df.copy()

# check accuraatheid
import numpy as np

# haal alle 30 scores weg, is geen neutral in RoBERTa
df = df[df['rating']!=30]

df['acc'] = np.where(
    (
        (df['rating']<30) & (df['sentiment']=='Negative')
    ) | ( 
        (df['rating']>30) & (df['sentiment']=='Positive')
    )
    ,1,0)

df['acc_cl'] = np.where(
    (
        (df['rating']<30) & (df['sentiment_cl']=='Negative')
    ) | ( 
        (df['rating']>30) & (df['sentiment_cl']=='Positive')
    )
    ,1,0)

# resultataat! Alle reviews
print('Accuraatheid van model op ongeschoonde data:',round(sum(df['acc'])/len(df)*100),'%')
print('Accuraatheid van model op geschoonde data:',round(sum(df['acc_cl'])/len(df)*100),'%')

# check met maximale lengte review
df2 = df[df['review'].str.len()<512]

# resultataat! Max lengte
print('Accuraatheid van model op ongeschoonde data:',round(sum(df2['acc'])/len(df2)*100),'%')
print('Accuraatheid van model op geschoonde data:',round(sum(df2['acc_cl'])/len(df2)*100),'%')