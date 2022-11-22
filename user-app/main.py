
########### EXAMPLE OF HOW THE CLASS WORKS !!! ###########
import pandas as pd
input_df = pd.DataFrame(
    {'test':[
        'Ik ben wel heel erg blij', 
        'ik ben super boos op jou', 
        'Wat ben jij een vervelende man', 
        'Waarom ben je niet liever voor me'
        ]})

# Run class wiht dataframe and columnname
sent_app = sentAnalysisApp(input_df,'test')

# return cleandata results from defenition CleanData
clean_df = sent_app.cleanData()

# Return results model a
model_a = sent_app.sentAnalysis(
                model_name='btjiong/robbert-twitter-sentiment',
                likert=3
                )

# Return results model b
model_b = sent_app.sentAnalysis(
        model_name='nlptown/bert-base-multilingual-uncased-sentiment',
        likert=5
        )   

# Return results single model
single_df = sent_app.runModel(model_type='single')

# Return results combined model
combined_df = sent_app.runModel()


if __name__ == "__main__":

    # DEFINE COLNAME 
    df = '''YOUR FILE PATH'''
    colname = '''DEFINE YOUR COLNAME '''

    from scripts.sentiment import sentAnalysisApp
    sent_app = sentAnalysisApp(df,colname)
    df_t = sent_app.runModel()

    # SAVE TO LOCATION
    df_t.to_csv(
        '''ENTER YOUR FILE OUTPUT LOCATION AND FILNAME''',
        sep=';',
        encoding='UTF-8-sig',
        index=False
        )

    