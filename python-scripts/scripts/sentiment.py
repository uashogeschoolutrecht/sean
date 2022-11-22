def sentimentBoolean(t_df,accuracy, colname):
    '''NOTE TEKST TOEVOEGEN!!!!!!!!!!!!!!'''
    # voor meer info https://huggingface.co/DTAI-KULeuven/robbert-v2-dutch-sentiment?text=a.
    from transformers import RobertaTokenizer, RobertaForSequenceClassification
    from transformers import pipeline
    model_name = 'DTAI-KULeuven/robbert-v2-dutch-sentiment' 
    model = RobertaForSequenceClassification.from_pretrained(model_name)
    tokenizer = RobertaTokenizer.from_pretrained(model_name)

    # classifier instellen
    classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

    df = t_df.copy()
    # set label
    n= 1
    df['label_onderwerp_{}'.format(n)] = ''
    df['score_onderwerp_{}'.format(n)] = 0

    # sentiment laden voor elke onderwerp kolom per rij (max length voor model is 512)
    c = colname
    for i in df.index:
        if len(df[c][i]) > 30 and len(df[c][i]) < 900:
            temp = classifier(df[c][i])
            df['label_onderwerp_{}'.format(n)][i] = temp[0]['label']
            df['score_onderwerp_{}'.format(n)][i] = temp[0]['score']

    # Lege waardes verwijderen 

    df = df[df['label_onderwerp_{}'.format(n)] != '']
    # alles met een accuracy onder de 95% weggooien
    df = df[df['score_onderwerp_{}'.format(n)] >= accuracy]

    return df


def sentimentLikert(t_df, colname,scale=3):
    '''This defenitions scores sentiment based on a likert scale. This is either on a 3 point or 
    5 point scale (default is 3 point), for the 3 point scale a twitter based model is used:
    https://huggingface.co/btjiong/robbert-twitter-sentiment?text=a. This model is spicificly 
    trained for dutch text. 
    The 5 point scale uses a model that is multilingual:
    https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment?text=a.'''
    df = t_df.copy()
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from scipy.special import softmax

    if scale == 3:
        model_name = 'btjiong/robbert-twitter-sentiment'
    else:
        model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'

    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # set labels either 3 point or 5 points
    if scale == 3:
        labels = ['Negative', 'Neutral', 'Positive',]
    else:
        labels = ['Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']

    # definieer kolom naam
    c = colname
    
    # labels toevoegen als kolommen
    for l in labels:
        df[l] = 0.00

    for i in df.index:
        if len(df[c][i]) > 30 and len(df[c][i]) < 900:
            test_txt = df[c][i]

            # tokinize
            encoded_text = tokenizer(test_txt , return_tensors='pt')

            # sentiment analysis
            output = model(**encoded_text)

            scores = output[0][0].detach().numpy()
            scores = softmax(scores)

            for l,s in zip(labels,scores):
                df[l][i] = s
    
    # drop empty values
    df.loc[:,'total'] = df[labels].sum(numeric_only=True, axis=1)    
    df = df[df['total']>0]
    df.drop(columns='total', inplace=True)

    return df
