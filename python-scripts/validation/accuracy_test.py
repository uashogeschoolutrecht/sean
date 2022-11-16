######################### MODEL TESTING ON TRIPADVISOR REVIEWS #########################
from scraper.tripadvisorscraper import hotelScraper

# vul een hotel url in
url = 'https://www.tripadvisor.nl/Hotel_Review-g188575-d230890-Reviews-Amrath_Grand_Hotel_de_l_Empereur-Maastricht_Limburg_Province.html#REVIEWS'

df = hotelScraper(url)

df.reset_index(drop=True, inplace=True)

# backupmaken 
df_backup = df.copy()

# zoveel mogelijk troep weggooien voor elke kolom
import sys
import os
os.chdir(r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\python-scripts\scripts')

from cleaning import schoonmaken
from cleaning import multiToSingleSpace

# cijfer en andere tekens verwijderen
df_rev = schoonmaken(df,'review')
df_rev = multiToSingleSpace(df_rev,'review')

# reset index
df_rev.reset_index(drop=True, inplace=True)

# alle lege reviews weglaten
df = df[~df['review'].isnull()]

######################### RUN MODELS ON REVIEWS #########################

##############5 points scale model

from sentiment import sentimentLikert
df_sent_likert = sentimentLikert(df_rev,'review', scale=5)

# copy used later for recode into 3 point scale
df_sent_5p = df_sent_likert.copy()

# rename review rating to match string values 
import numpy as np 
    
# Mapping number to values
conditions = [
    df_sent_likert['rating']==10,
    df_sent_likert['rating']==20,
    df_sent_likert['rating']==30,
    df_sent_likert['rating']==40,
    df_sent_likert['rating']==50
    ]

choices = ['Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']
df_sent_likert['rating'] = np.select(conditions, choices, default=df_sent_likert['rating'])


# get the row name of the highest value 
df_sent_likert['max_sentiment'] = df_sent_likert[[
    'Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']].idxmax(axis=1)

# get accuracy
df_sent_likert['accuracy'] = np.where(
    df_sent_likert['max_sentiment']==df_sent_likert['rating'],1,0)


# check only extremes
df_sent_likert_extremes = df_sent_likert[df_sent_likert['max_sentiment'].str.contains('Very')]


# set def for remapping reviews score to 3 pointscale
def acc3points(df):
    # Mapping number to values
    df_t = df.copy()
    conditions = [
        df_t['rating']==10,
        df_t['rating']==20,
        df_t['rating']==30,
        df_t['rating']==40,
        df_t['rating']==50
        ]

    choices = ['Negative', 'Negative', 'Neutral', 'Positive', 'Positive']
    df_t['rating'] = np.select(conditions, choices, default=df_t['rating'])

    # get the row name of the highest value 
    df_t['max_sentiment'] = df_t[[
        'Negative', 'Neutral', 'Positive']].idxmax(axis=1)

    # get accuracy
    df_t['accuracy'] = np.where(
        df_t['max_sentiment']==df_t['rating'],1,0)

    return df_t

############# 3 points scale model 
df_sent_3p = sentimentLikert(df_rev,'review', scale=3)

df_sent_3p_sc = acc3points(df_sent_3p)

import pandas as pd 
df_rev = pd.read_csv('tripadivsordata.csv', sep=';')
df_rev.drop(columns='Unnamed: 0',inplace=True)

############# recode 5 pointscale to 3 point
labels = ['Negative', 'Neutral', 'Positive']

import numpy as np
df_sent_5p['Positive'] = df_sent_5p['Very positive']+df_sent_5p['Positive']
df_sent_5p['Negative'] = df_sent_5p['Very negative']+df_sent_5p['Negative']
df_sent_5p.drop(columns=['Very negative', 'Very positive'],inplace=True)

df_sent_5p_sc = acc3points(df_sent_5p)


############# combine models for an average score
# rename labels before merge
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
df_2models_sc = acc3points(df_2models)

# resultataat! Alle reviews
print('Accuracy test for sentiment analysis models on Tripadvisor data (n=229) ')
print('Accuracy for bert-base-multilingual-uncased-sentiment:')
print('-------------------------------------------------------------------------------')
print('Accuracy of model on cleaned data:',round(sum(df_sent_likert['accuracy'])/len(df_sent_likert)*100),'%')
# resultataat! for extremes
print('Accuracy of model for extremes (Very positive/negative):',round(sum(df_sent_likert_extremes['accuracy'])/len(df_sent_likert_extremes)*100),'%')
# results for recoded to 3 pointscale 
print('Accuracy of model for recoded values to 3 pointscale:',round(sum(df_sent_5p_sc['accuracy'])/len(df_sent_5p_sc)*100),'%')
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
