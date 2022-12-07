
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

    