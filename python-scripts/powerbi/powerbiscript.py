'''Scripts kunnen direct ingeladen worden in Powerbi het is echter niet mogelijk om met
een mappen scructuur te werken zoals in VSCODE, daarom is het noodzakelijk om alles onder 
elkaar te plakken.'''

###### functies
def connectDB(db): 
    
    '''This function is used to connect to the HU server. 
    Please provide a valid database name in order to connect'''

    import pymssql 
    connect = pymssql.connect(
        server='DBND25.medewerkers.ad.hvu.nl',
        database=db)

    return connect


# functie om stopworden te verwijderen
def schoonmaken(df, col):

    # Nederlandse stopworden inladen
    from nltk.corpus import stopwords
    stopwoorden_nl = stopwords.words('dutch')
    
    # kolommen omzetten naar string
    df[col] = df[col].astype(str)

    # Houd enkel nog woorden over
    df[col] = df[col].str.replace('[^A-z]', ' ')

    # stopwoorden verwijderen
    df[col] = df[col].apply(lambda x: ' '.join(x for x in x.split() if x not in stopwoorden_nl))

    # Lemmatization
    from textblob import Word
    df[col] = df[col].apply(lambda x: ' '.join([Word(x).lemmatize() for x in x.split()]))

    return df



# connectie maken met database (default is nu op 25)
conn = connectDB(db='TOPDESK_SAAS')

# sql query
sql = '''SELECT TOP (1000) inc.unid AS id
        ,srt.naam AS melding
        ,[actie]
        ,verzoek 
        ,ref_domein
    FROM [dbo].[incident] AS inc
    LEFT JOIN soortbinnenkomst AS srt ON srt.unid = inc.soortbinnenkomstid
    LEFT JOIN actiedoor AS ad ON ad.unid = inc.operatorgroupid
    WHERE datumaangemeld >= '2021-01-01'
        AND ad.naam = 'OL-STIP'
        AND srt.naam = 'E-Mail'
'''

import pandas as pd
# sql inladen en omzetten naar dataframe
bev_df = pd.read_sql_query(sql, conn)

# connectie aflsuiten
conn.close()

# file zonder id voor anayse 
df = pd.DataFrame(bev_df[['melding','verzoek','actie', 'ref_domein']])

# opschonen van bestand
df['verzoek'] = df['verzoek'].str.lower()

# bekijk de lengte van elk verzoek
df['len_verzoek'] = df['verzoek'].str.len()

# tel aantal email berichten aan de hand van de keren dat het woord onderwerp: voorkomt
df['onderwerp_count'] = df['verzoek'].str.count(r'(onderwerp:|subject:)')

# lengte van de spit
split_len = max(df['onderwerp_count'])

# aantal kolommen uitbreiden met max aantal keer dat onderwerp voorkomt
cols = list()
for i in range(split_len+1):
    cols += ['onderwerp_{}'.format(i)]
    

# onderwerp teksten als aparte kolommen toevoegen
df[cols] = df['verzoek'].str.split('onderwerp:', expand=True)

# eerste uitbreiding weggooien bevat alleen infor van voor het woord onderwerp
df.drop(columns='onderwerp_0', inplace=True)

# zoveel mogelijk troep weggooien voor elke kolom
for c in cols[1:]:
    # eerst alle line braks omzetten naar ###
    df[c] = df[c].str.replace(r'\n',' ### ')
    df[c] = df[c].str.replace(r'(met vriendelijke groet.*|mvg.*|kind regards.*)','')
    df[c] = df[c].str.replace(r'van:.*?verzonden:.*?aan:.*','')
    df[c] = df[c].str.replace(r' ### ','\n')

    # cijfer en andere tekens verwijderen, stopwoorden verwijderen
    df = schoonmaken(df,c)
    df[c] = df[c].str.replace('None','')

# index ressetten voor de zekerheid
df.reset_index(inplace=True, drop=True)


### Sentiment analyse van opgeschoond bestand met opgeschooonde bestand 
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import pipeline
import torch

# model instellen
model_name = 'DTAI-KULeuven/robbert-v2-dutch-sentiment'
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

# classifier instellen
classifier = pipeline('sentiment-analysis', model=model, tokenizer = tokenizer)

# label en score kolommen toevoegen
for n in range(1,split_len+1):
    df['label_onderwerp_{}'.format(n)] = ''
    df['score_onderwerp_{}'.format(n)] = 0

# sentiment laden voor elke onderwerp kolom per rij
n = 1
for c in cols[1:]:
    for i in df.index:
        if len(df[c][i]) > 30 and len(df[c][i]) < 2000:
            temp = classifier(df[c][i])
            df['label_onderwerp_{}'.format(n)][i] = temp[0]['label']
            df['score_onderwerp_{}'.format(n)][i] = temp[0]['score']
    n +=1

# volgorde kolommen aanpassen
col_order = ['melding','verzoek','actie','ref_domein', 'len_verzoek', 'onderwerp_count']

# kolommen toevoegen op basis van lengte van split
for n in range(1,split_len+1):
    col_order += ['onderwerp_{}'.format(n)] 
    col_order += ['label_onderwerp_{}'.format(n)]
    col_order += ['score_onderwerp_{}'.format(n)] 

# df voor output beschikbaar stellen
df = df[col_order]

# als nederlandse versie van python 
for n in range(1,split_len+1):
    col = ['score_onderwerp_{}'.format(n)]    
    df[col] = df[col].mul(100)
    df[col] = df[col].round()
    df[col] = df[col].astype(int)

del bev_df, c, classifier, col_order, cols, i, model, model_name, n, split_len, temp, tokenizer, conn, sql, col