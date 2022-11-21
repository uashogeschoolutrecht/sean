if __name__ == "__main__":
    # load data from csv
    from scripts.readfiles import readCsv
    df = readCsv('tripadivsordata')

    # run sentiment analysis 
    from scripts.sentiment import sentAnalysisApp
    sent_app = sentAnalysisApp(df,'review')

    # choose the model tipe?
    results_likert = sent_app.runModel()
    results_bool = sent_app.sentAnalysisReviews()
    
    results_likert.to_csv(
        r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\user-app\input\sentimentresults.csv',
        sep=';',
        encoding='UTF-8-sig',
        index=False
        )

    results_bool.to_csv(
        r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\user-app\input\sentimentresults_roberta.csv',
        sep=';',
        encoding='UTF-8-sig',
        index=False
        )

