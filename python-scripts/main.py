####################################################################
# Titel         : "Sean: the HU sentimenent analysis algorithm"
# Auteur        : Anne Leemans
# Start datum   : 27/10/2022
# Python versie : Python 3.10.7
####################################################################

########################################################################
### Sentiment analyse van opgeschoond bestand met opgeschooonde bestand 
########################################################################
from other.get_files import loadTable

# geschoonde data inladen
clean_data = loadTable()

df = clean_data.copy()

# hulp objecten inladen
split_len = max(df['onderwerp_count'])
cols = df.columns[7:].values.tolist()

# model instellen
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import pipeline
model_name = 'DTAI-KULeuven/robbert-v2-dutch-sentiment' # voor meer info https://huggingface.co/DTAI-KULeuven/robbert-v2-dutch-sentiment?text=Ik+erken+dat+dit+een+boek+is%2C+daarmee+is+alles+gezegd.
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

# classifier instellen
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# label en score kolommen toevoegen
for n in range(1,split_len):
    df['label_onderwerp_{}'.format(n)] = ''
    df['score_onderwerp_{}'.format(n)] = 0

# sentiment laden voor elke onderwerp kolom per rij (max length voor model is 512)
n = 1
for c in cols:
    for i in df.index:
        if len(df[c][i]) > 30 and len(df[c][i]) < 512:
            temp = classifier(df[c][i])
            df['label_onderwerp_{}'.format(n)][i] = temp[0]['label']
            df['score_onderwerp_{}'.format(n)][i] = temp[0]['score']
    n +=1

# volgorde kolommen aanpassen
col_order = df.columns[:7].values.tolist()

# kolommen toevoegen op basis van lengte van split
for n in range(1,split_len):
    col_order += ['onderwerp_{}'.format(n)] 
    col_order += ['label_onderwerp_{}'.format(n)]
    col_order += ['score_onderwerp_{}'.format(n)] 

# df voor output beschikbaar stellen
df = df[col_order]

del c, classifier, col_order, cols, i, model, model_name, n, split_len, temp, tokenizer

#################################################
# Data prepareren voor visualisatie
# naar specificatie 
ref_specs = df.groupby(['ref_specificatie','label_onderwerp_1']).size()

# omzetten naar dataframe
import pandas as pd
ref_specs = pd.DataFrame(ref_specs.reset_index(name='aantal'))

# lege waarde classifeseren als neutraal (niet classificeerbaar)
import numpy as np
ref_specs['label_onderwerp_1'] = np.where(ref_specs['label_onderwerp_1']=='','Neutral',ref_specs['label_onderwerp_1'])

ref_specs.rename(columns={'label_onderwerp_1':'sentiment', 'ref_specificatie': 'thema'},inplace=True)

# maak een lijst met nieuwe kolom namen
cols = ref_specs['sentiment'].drop_duplicates().values.tolist()

# reframe dataframe
df_specs = ref_specs[['thema']].drop_duplicates()

for c in cols:
    temp = ref_specs[ref_specs['sentiment']==c][['thema','aantal']]
    temp.rename(columns={'aantal':c},inplace=True)
    df_specs = df_specs.merge(temp, 'left')

df_specs['Totaal'] =df_specs[cols].sum(axis=1)
df_specs.sort_values('Totaal', ascending=False, inplace=True)

df_specs['cul_neutral'] =df_specs[['Negative','Neutral']].sum(axis=1)

del cols, c, temp


#################################################
#### Visualisatie
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(6, 15))

# Plot totaal aantal waardes
sns.set_color_codes("pastel")
sns.barplot(x="Totaal", y="thema", data=df_specs,
            label="Positief", color="#089000")


# Plot aantal negatieve
sns.set_color_codes("muted")
sns.barplot(x="cul_neutral", y="thema", data=df_specs,
            label="Neutraal", color="#f1c232")

# Plot aantal negatieve
sns.set_color_codes("muted")
sns.barplot(x="Negative", y="thema", data=df_specs,
            label="Negatief", color="#cc0000")
          

# Legenda toevoegen
ax.legend(ncol=3, loc="lower right", frameon=True)
ax.set(xlim=(0, max(df_specs['Totaal']+10)), ylabel="",
       xlabel="Aantal geclassificeerde onderwerpen")
sns.despine(left=True, bottom=True)


