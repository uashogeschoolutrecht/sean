class sentAnalysisApp:
    '''NOTE ADD CLASS INGO'''
    def __init__(self,dtframe,colname):
        self.dtaframe = dtframe
        self.colname = colname
        self.labels = ['Negative', 'Neutral', 'Positive',]

    def cleanData(self,dtframe,colname):
        '''Some genereal data preperation, remove all symbols and numbers.
        transforms all text to lower case and removes redundant and trailing 
        spaces.
        '''

        # set values to srting
        df = dtframe.copy()
        df[colname] = df[colname].astype(str)

        # remove all line breaks
        df[colname] = df[colname].str.replace(r'\n',' ')

        # all to lowercase 
        df[colname] = df[colname].str.lower()

        # remove all symbols and numbers
        df[colname] = df[colname].str.replace('[^A-záéíóúýçäëïöüÿàèìòùâêîôûãõñ]', ' ')

        while df[colname].str.find('  ').sum() > 0:
            df[colname] = df[colname].str.replace('  ', ' ')

        return df

    def sentAnalysis(self,dt_f,colname,model_name,likert): 
        '''This defenitions scores sentiment based on a likert scale. This is either on a 3 point or 
        5 point scale (default is 3 point), for the 3 point scale a twitter based model is used:
        https://huggingface.co/btjiong/robbert-twitter-sentiment?text=a. This model is spicificly 
        trained for dutch text. 
        The 5 point scale uses a model that is multilingual:
        https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment?text=a.'''   
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        from scipy.special import softmax
        df = dt_f.copy()

        # set model
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # definieer kolom naam
        c = colname

        # labels toevoegen als kolommen
        for l in self.labels:
            df[l] = 0.00

        for i in df.index:
            # skip all text that have less then 30 or more than 900 characters
            if len(df[c][i]) > 30 and len(df[c][i]) < 900:
                
                sent_text = df[c][i]

                # tokinize
                encoded_text = tokenizer(sent_text , return_tensors='pt')

                # sentiment analysis
                output = model(**encoded_text)

                # get scores from sentiment
                scores = output[0][0].detach().numpy()
                scores = softmax(scores)
                
                # if model uses a 5 points scale, recode to 3 points
                if likert == 5:
                    import numpy as np
                    scores = np.array([scores[0:2].sum()]+[scores[2]]+[scores[3:5].sum()])

                for l,s in zip(self.labels,scores):
                    df[l][i] = s

        # drop empty values
        df.loc[:,'total'] = df[self.labels].sum(numeric_only=True, axis=1)    
        df = df[df['total']>0]
        df.drop(columns='total', inplace=True)

        return df

    def combineModels(self):         
        # clean data
        df = self.cleanData(self.dtaframe,self.colname)

        # set models
        models = [
            'btjiong/robbert-twitter-sentiment',
            'nlptown/bert-base-multilingual-uncased-sentiment'
        ]

        # sentiment op model a
        df_a = self.sentAnalysis(
            dt_f=df,colname=self.colname,model_name=models[0],likert=3)
        
        # sentiment op model b
        df_b = self.sentAnalysis(
            dt_f=df,colname=self.colname,model_name=models[1],likert=5)


        # combine models for an average score
        for l in self.labels:
            df_a.rename(columns={l:'{}_a'.format(l)}, inplace=True)
            df_b.rename(columns={l:'{}_b'.format(l)}, inplace=True)

        # drop review and rating column
        df_b.drop(columns=['rating','review'], inplace=True)

        # join dataframes
        df_combined =  pd.concat([df_a, df_b], axis=1)

        # combine columns to one
        for l in self.labels:
            df_combined[l] = (df_combined['{}_a'.format(l)] + df_combined['{}_b'.format(l)])/2

        # drop old colums
        for l in self.labels:
            df_combined.drop(columns=['{}_a'.format(l),'{}_b'.format(l)],inplace=True)

        # set sentiment score
        df_combined['sentiment'] = round(df_combined['Positive'] - df_combined['Negative'],2)

        # drop seperate columns 
        df_combined.drop(columns=self.labels,inplace=True)

        return df_combined


    def sentimentVisDfLikert(self, df,subject):
        '''Deze defenitie prepareert data van een sentiment analyse voor visualisatie
        NOTE! deze functie kan alleen gebruikt worden voor sentiment die gebruik maakt 
        van een likert scale weergeeft'''

        temp_df = df.copy()

        # grouperen naar gekozen onderwerp
        temp_df = temp_df[[subject]+self.labels].groupby(subject).mean()
        temp_df.reset_index(inplace=True)
        
        # aantallen telleven voor sortering
        aantal = df.copy()
        aantal = aantal.groupby([subject]).size()

        # series to dataframe
        temp_df = temp_df.merge(aantal.reset_index(), 'left')

        # sort naar aantal
        temp_df.sort_values(0, ascending=False, inplace=True)

        # omzetten naar dataframe
        import pandas as pd
        temp_df.reset_index(inplace=True, drop=True)
        temp_df.rename(columns={subject: 'thema', 0: 'aantal'},inplace=True)

        # Cul waardes maken    
        for i in range(1,len(self.labels)+1):
            temp_df['{}_cul'.format(self.labels[i-1])] = temp_df.loc[:,self.labels[0:i]].sum(axis=1)


        return temp_df

    def plotResults(self):

        #NOTE WORK IN PROGRESS!!
        # sentiment = sentAnalysisApp(df_rev,'review')

        # results = sentiment.combineModels()
        # results.to_csv('tripadivsordata_metscore.csv',sep=';',encoding='UTF-8-sig',index=False)


        # hotels = ['Linden Hotel', 'Super strip', 'Fietshotel', 'Grand hall', 'Hotel off lights', 'City hotel', 'In de zon']

        # df_h = pd.DataFrame({'hotelname':hotels})

        # for i in range (327):
        #     df_h = df_h.append(pd.DataFrame({'hotelname':hotels}))

        # df_h.reset_index(drop=True,inplace=True)


        # results =  pd.concat([df_h, df], axis=1)
        # results = results[['hotelname','sentiment']]
        # neg = results[results['sentiment']<0]
        # pos = results[results['sentiment']>0]

        # neg = neg.groupby('hotelname').mean()
        # pos = pos.groupby('hotelname').mean()
        # neg.reset_index(inplace=True)
        # pos.reset_index(inplace=True)

        # ### VIS
        # import matplotlib.pyplot as plt
        # import seaborn as sns

        # # Change default style
        # sns.set_style('white')
        # # Change default context
        # sns.set_context('notebook') 

        # sentiment_hue = results.eval("sentiment / rating").rename("sentiment")
        # f, ax = plt.subplots(figsize=(6.5, 6.5))
        # ax.grid(False)
        # ax.set(
        #     xlabel='tripadvisore rating',    
        #     ylabel='sentiment score from combined models')
            
        # sns.despine(f, left=True, bottom=True)

        # # titel toevoegen
        # scat = sns.scatterplot(    
        #     data=results, 
        #     y="sentiment", 
        #     x= 'rating', 
        #     hue=sentiment_hue, 
        #     palette= sns.color_palette("Spectral", as_cmap=True), 
        #     legend=False,
        #     linewidth=0, 
        #     ax=ax
        #     )


        # from scipy.stats import pearsonr
        # import numpy as np
        # corr, _ = pearsonr(np.array(results['sentiment']), np.array(results['rating']))

        # scat.axes.set_title(
        #     label=' Tripadvisor test:\n Reviewscore naar sentiment score (n=2296)\n{}\n'.format('Pearsons correlation: %.3f' % corr),fontsize=13)
        print('results')
