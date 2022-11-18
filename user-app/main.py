if __name__ == "__main__":
    # load data from csv
    from scripts.readfiles import readCsv
    df = readCsv('tripadivsordata',nrows=100)

    # run sentiment analysis 
    from scripts.sentiment import sentAnalysisApp
    sent_app = sentAnalysisApp(df,'review')
    results = sent_app.runModel()
    
    results.to_csv(
        filepath_or_buffer=r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\user-app\input\sentimentresults.csv',
        sep=';',
        encoding='UTF-8-sig',
        index=False
        )

