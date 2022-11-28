########################## LOAD TEST DATA FROM TRIPADIVSOR #########################
import pandas as pd 
df_rev = pd.read_csv(r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\user-app\input\tripadivsordata.csv', sep=';',nrows=10)

def numberToValue(input_df,choices):
    '''Changes rating numbers to values for comparing'''
    import numpy as np
    df = input_df.copy()
    conditions = [
        df['rating']==10,
        df['rating']==20,
        df['rating']==30,
        df['rating']==40,
        df['rating']==50
        ]
    df['rating'] = np.select(conditions, choices, default=df['rating'])

    return df


########################## RUN MODELS ON REVIEWS #########################
############## boolean  model
import os
os.chdir(r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\user-app\scripts')
from sentiment import sentAnalysisApp
sent_app = sentAnalysisApp(df_rev,'review')
df_sent_bool = sent_app.sentAnalysisReviews()

choices = ['Negative', 'Negative', 'Neutral', 'Positive', 'Positive']

# rating numbers to strings
df_sent_bool = numberToValue(df_sent_bool,choices)

# remove neutral values (not in model)
df_sent_bool = df_sent_bool[df_sent_bool['rating']!='Neutral']

import numpy as np
df_sent_bool['accuracy'] = np.where(
    df_sent_bool['label_onderwerp_1']==df_sent_bool['rating'],1,0)


############## 5 points scale model
from sentiment import sentimentLikert
df_sent_5p = sentimentLikert(df_rev,'review', scale=5)

# copy used later for recode into 3 point scale
df_sent_5_to_3p = df_sent_5p.copy()

choices = ['Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']
# rating numbers to strings
df_sent_5p = numberToValue(df_sent_5p,choices)

# get the row name of the highest value 
df_sent_5p['max_sentiment'] = df_sent_5p[[
    'Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']].idxmax(axis=1)

# get accuracy
df_sent_5p['accuracy'] = np.where(
    df_sent_5p['max_sentiment']==df_sent_5p['rating'],1,0)

# check only extremes
df_sent_5p_extremes = df_sent_5p[df_sent_5p['max_sentiment'].str.contains('Very')]


############# recode 5 pointscale to 3 point
df_sent_5_to_3p['Positive'] = df_sent_5_to_3p['Very positive']+df_sent_5_to_3p['Positive']
df_sent_5_to_3p['Negative'] = df_sent_5_to_3p['Very negative']+df_sent_5_to_3p['Negative']
df_sent_5_to_3p.drop(columns=['Very negative', 'Very positive'],inplace=True)

choices = ['Negative', 'Negative', 'Neutral', 'Positive', 'Positive']
df_sent_5_to_3p_sc = numberToValue(df_sent_5_to_3p,choices)

# get the row name of the highest value 
df_sent_5_to_3p_sc['max_sentiment'] = df_sent_5_to_3p_sc[[
    'Negative', 'Neutral', 'Positive']].idxmax(axis=1)

# get accuracy
df_sent_5_to_3p_sc['accuracy'] = np.where(
    df_sent_5_to_3p_sc['max_sentiment']==df_sent_5_to_3p_sc['rating'],1,0)


############# 3 points scale model 
df_sent_3p = sentimentLikert(df_rev,'review', scale=3)

choices = ['Negative', 'Negative', 'Neutral', 'Positive', 'Positive']
df_sent_3p_sc = numberToValue(df_sent_3p,choices)

# get the row name of the highest value 
df_sent_3p_sc['max_sentiment'] = df_sent_3p_sc[[
    'Negative', 'Neutral', 'Positive']].idxmax(axis=1)

# get accuracy
df_sent_3p_sc['accuracy'] = np.where(
    df_sent_3p_sc['max_sentiment']==df_sent_3p_sc['rating'],1,0)


############# combine models for an average score
# rename labels before merge
labels = ['Negative', 'Neutral', 'Positive']

for l in labels:
    df_sent_3p.rename(columns={l:'{}_3p'.format(l)}, inplace=True)
    df_sent_5p.rename(columns={l:'{}_5p'.format(l)}, inplace=True)

# drop review and rating column
df_sent_5p.drop(columns=['rating','review'], inplace=True)

# join dataframes
df_2models =  pd.concat([df_sent_3p, df_sent_5p], axis=1)

# combine columns to one
for l in labels:
    df_2models[l] = (df_2models['{}_3p'.format(l)] + df_2models['{}_5p'.format(l)])/2

# drop old colums
for l in labels:
    df_2models.drop(columns=['{}_3p'.format(l),'{}_5p'.format(l)],inplace=True)

# get scores from combined models
df_2models_sc = numberToValue(df_2models,choices)

# get the row name of the highest value 
df_2models_sc['max_sentiment'] = df_2models_sc[[
    'Negative', 'Neutral', 'Positive']].idxmax(axis=1)

# get accuracy
df_2models_sc['accuracy'] = np.where(
    df_2models_sc['max_sentiment']==df_2models_sc['rating'],1,0)



# resultataat! Alle reviews
print('Accuracy test for sentiment analysis models on Tripadvisor data (n=2296) ')
# resultataat! Alle reviews
print('Accuracy for DTAI-KULeuven/robbert-v2-dutch-sentiment: ')
print('-------------------------------------------------------------------------------')
print('Accuracy of model on cleaned data:',round(sum(df_sent_bool['accuracy'])/len(df_sent_bool)*100),'%')
print('-------------------------------------------------------------------------------\n')

print('Accuracy for bert-base-multilingual-uncased-sentiment:')
print('-------------------------------------------------------------------------------')
print('Accuracy of model on cleaned data:',round(sum(df_sent_5p['accuracy'])/len(df_sent_5p)*100),'%')
# resultataat! for extremes
print('Accuracy of model for extremes (Very positive/negative):',round(sum(df_sent_5p_extremes['accuracy'])/len(df_sent_5p_extremes)*100),'%')
# results for recoded to 3 pointscale 
print('Accuracy of model for recoded values to 3 pointscale:',round(sum(df_sent_5_to_3p_sc['accuracy'])/len(df_sent_5_to_3p_sc)*100),'%')
print('-------------------------------------------------------------------------------\n')

# resultataat! Alle reviews
print('Accuracy for btjiong/robbert-twitter-sentiment: ')
print('-------------------------------------------------------------------------------')
print('Accuracy of model on cleaned data:',round(sum(df_sent_3p_sc['accuracy'])/len(df_sent_3p_sc)*100),'%')
print('-------------------------------------------------------------------------------\n')

# resultataat! Combined models
print('Accuracy for robbert-twitter & bert-multilingual combined: ')
print('-------------------------------------------------------------------------------')
print('Accuracy for model on cleaned data:',round(sum(df_2models_sc['accuracy'])/len(df_2models_sc)*100),'%')
print('-------------------------------------------------------------------------------')



