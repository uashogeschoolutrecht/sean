
########################## LOAD HU TEST DATA #########################
#1. Import data
import os
os.chdir(r'/home/{}/scratch/sean/user-app/scripts/'.format(os.getlogin()))

from readfiles import readfileRD 
data_exit = readfileRD('2022sean', 'exit') 
data_topdesk = readfileRD('2022sean', 'topdesk')

# filter data: only keep annotated datarows
df_only_ann = data_exit[data_exit['annotation'].notna()]

#2. Run sentiment app on data
from sentiment import sentAnalysisApp

sent_app = sentAnalysisApp(df_only_ann,'Text')
df_sent_bool = sent_app.sentAnalysisReviews()

# Look at results
import matplotlib.pyplot as plt
plt.hist(x=df_sent_bool['annotation'], bins=10)
plt.show()

import scipy
scipy.stats.shapiro(df_sent_bool['annotation'])
# annotated data seems normally distributed (p < 0.05), however, 
# sample size (N~50) is far too small for conclusive evidence.

scipy.stats.pearsonr(df_sent_bool['annotation'], df_sent_bool['sentiment'])
plt.scatter(df_sent_bool['annotation'], df_sent_bool['sentiment'])