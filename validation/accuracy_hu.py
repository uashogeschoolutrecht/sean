
########################## LOAD HU TEST DATA #########################
#1. Import data
import os
os.chdir(r'/home/{}/scratch/sean/user-app/scripts/'.format(os.getlogin()))

from readfiles import readfileRD 
data_hu = readfileRD('2022sean', 'exit') #'topdesk' is also available as file

# filter data: only keep annotated datarows
df_only_ann = data_hu[data_hu['annotation'].notna()]

#2A. Run sentiment app on data [MODEL BOOL]
from sentiment import sentAnalysisApp

sent_app = sentAnalysisApp(df_only_ann,'Text')
df_sent_bool = sent_app.sentAnalysisReviews()
import matplotlib.pyplot as plt

#visualise sentiment scores
fig, axs = plt.subplots(2)
fig.suptitle('Sentiment score distributions')
axs[0].plot(df_sent_bool['sentiment'], 'o')
axs[1].hist(x=df_sent_bool['sentiment'], bins=10)
# unclear why results of algoritm are skewed to both ends of the spectrum (-1, 1). 

# Look at annotations
plt.hist(x=df_sent_bool['annotation'], bins=10)
plt.show()
import scipy
scipy.stats.shapiro(df_sent_bool['annotation'])
# annotated data seems normally distributed (p < 0.05), however, 
# sample size (N~50) is far too small for conclusive evidence.

scipy.stats.pearsonr(df_sent_bool['annotation'], df_sent_bool['sentiment'])
plt.scatter(df_sent_bool['annotation'], df_sent_bool['sentiment'])
# Correlation coefficient ~0.50 is not found in a visual representation of the data. 

#2B. Run sentiment app on data [MODEL ROBBERT]
df_sent_rob = sent_app.sentAnalysis(
                                    model_name='btjiong/robbert-twitter-sentiment',
                                    likert=3)

#Rescale answers & visualise
df_sent_rob['sentiment'] = df_sent_rob['Negative']*-1 + df_sent_rob['Positive']

fig, axs = plt.subplots(2)
fig.suptitle('Sentiment score distributions')
axs[0].plot(df_sent_rob['sentiment'], 'o')
axs[1].hist(x=df_sent_rob['sentiment'], bins=10)
# Results of algoritm are skewed toward the positive end of the scale (1), but comparing 
# the model with the Boolean results, sentiment scores are more uniformly distributed. 

scipy.stats.pearsonr(df_sent_rob['annotation'], df_sent_rob['sentiment'])
plt.scatter(df_sent_rob['annotation'], df_sent_rob['sentiment'])

#2C. Run sentiment app on data [MODEL BERT]
df_sent_bert = sent_app.sentAnalysis(
                                    model_name='nlptown/bert-base-multilingual-uncased-sentiment',
                                    likert=5)

#Rescale answers & visualise
df_sent_bert['sentiment'] = df_sent_bert['Negative']*-1 + df_sent_bert['Positive']

fig, axs = plt.subplots(2)
fig.suptitle('Sentiment score distributions')
axs[0].plot(df_sent_bert['sentiment'], 'o')
axs[1].hist(x=df_sent_bert['sentiment'], bins=10)
# Results of algoritm are roughly uniformly distributed. 

#scipy.stats.pearsonr(df_sent_bert['annotation'], df_sent_bert['sentiment'])
plt.scatter(df_sent_bert['annotation'], df_sent_bert['sentiment'])
