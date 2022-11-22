

class sentAnalysisApp:
    '''NOTE ADD CLASS INFO --> NAME CHANGES PLUS MORE INFO FOR EACH INDIVIDUAL DEFINITION'''
    def __init__(self,dtframe,colname):
        self.dtaframe = dtframe
        self.colname = colname
        self.labels = ['Negative', 'Neutral', 'Positive']


    def cleanData(self):
        '''Some genereal data preperation, remove all symbols and numbers.
        transforms all text to lower case and removes redundant and trailing 
        spaces.
        '''
        df = self.dtaframe.copy()
        colname = self.colname

        import pandas as pd
        pd.options.mode.chained_assignment = None  # default='warn'

        # supress future warnings
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)


        # set values to srting
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

     
     
    def sentAnalysis(self,model_name,likert): 
        '''This defenitions scores sentiment based on a likert scale. This is either on a 3 point or 
        5 point scale (default is 3 point), for the 3 point scale a twitter based model is used:
        https://huggingface.co/btjiong/robbert-twitter-sentiment?text=a. This model is spicificly 
        trained for dutch text. 
        The 5 point scale uses a model that is multilingual:
        https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment?text=a.
        '''   
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        from scipy.special import softmax
        df = self.dtaframe.copy()
        colname = self.colname
        labels = self.labels

        # set model
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
  
        # labels toevoegen als kolommen
        for l in labels:
            df[l] = 0.00

        for i in df.index:
            # skip all text that have less then 30 or more than 900 characters
            if len(df[colname][i]) > 15 and len(df[colname][i]) < 900:
                
                sent_text = df[colname][i]

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

                for l,s in zip(labels,scores):
                    df[l][i] = s

        # drop empty values
        df.loc[:,'total'] = df[labels].sum(numeric_only=True, axis=1)    
        df = df[df['total']>0]
        df.drop(columns='total', inplace=True)

        # reset index
        df.reset_index(drop=True, inplace=True)

        return df

    def sentAnalysisReviews(self):
        '''This model is sepcifically trained on Duthc user reviews and can there for 
        be used on similair data. The model can be found here:
        https://huggingface.co/DTAI-KULeuven/robbert-v2-dutch-sentiment?text=a.
        '''
        # set model
        from transformers import RobertaTokenizer, RobertaForSequenceClassification
        from transformers import pipeline
        model_name = 'DTAI-KULeuven/robbert-v2-dutch-sentiment' 
        model = RobertaForSequenceClassification.from_pretrained(model_name)
        tokenizer = RobertaTokenizer.from_pretrained(model_name)

        # classifier instellen
        classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

        df = self.dtaframe.copy()
        colname = self.colname
        df['sentiment'] = 9999

        # sentiment laden voor elke onderwerp kolom per rij (max length voor model is 512)
        for i in df.index:
            if len(df[colname][i]) > 15 and len(df[colname][i]) < 900:
                temp = classifier(df[colname][i])
                if temp[0]['label'] == 'Negative':
                    df['sentiment'][i] = temp[0]['score']*-1
                else:
                    df['sentiment'][i] = temp[0]['score']


        # Lege waardes verwijderen 
        df = df[df['sentiment'] != 9999]

        # round score
        df['sentiment'] =  round(df['sentiment'],4)

        # reset index
        df.reset_index(drop=True, inplace=True)

        return df

    def runModel(self,model_type='combined'): 
        # clean data
        df = self.cleanData()

        # chcek model type
        if model_type == 'combined':

            # set models
            models = [
                'btjiong/robbert-twitter-sentiment',
                'nlptown/bert-base-multilingual-uncased-sentiment'
            ]

            # sentiment op model a
            df_a = self.sentAnalysis(
                model_name=models[0],likert=3)
            
            # sentiment op model b
            df_b = self.sentAnalysis(
                model_name=models[1],likert=5)


            # combine models for an average score
            for l in self.labels:
                df_a.rename(columns={l:'{}_a'.format(l)}, inplace=True)
                df_b.rename(columns={l:'{}_b'.format(l)}, inplace=True)
            
            # drop keep only the scores 
            df_b = df_b.iloc[:,-3:]
            # join dataframes
            import pandas as pd
            df_combined =  pd.concat([df_a, df_b], axis=1)

            # combine columns to one
            for l in self.labels:
                df_combined[l] = (df_combined['{}_a'.format(l)] + df_combined['{}_b'.format(l)])/2

            # drop old colums
            for l in self.labels:
                df_combined.drop(columns=['{}_a'.format(l),'{}_b'.format(l)],inplace=True)

            # set sentiment score
            df_combined['sentiment'] = round(df_combined['Positive'] - df_combined['Negative'],4)

            # drop seperate columns 
            df_combined.drop(columns=self.labels,inplace=True)

            # reset index
            df_combined.reset_index(drop=True, inplace=True)

            return df_combined

        else:
            df_r = self.sentAnalysisReviews()

            # reset index
            df_r.reset_index(drop=True, inplace=True)
            
            return df_r


