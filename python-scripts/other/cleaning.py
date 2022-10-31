# # eerst topwoordenlijsten downloaden NOTE! dit doe je maar eenkeer
# import nltk
# from pyparsing import col
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


# functie om stopworden te verwijderen
def schoonmaken(df, col):

    # Nederlandse stopworden inladen
    from nltk.corpus import stopwords
    stopwoorden_nl = stopwords.words('dutch')
    
    # kolommen omzetten naar string
    df[col] = df[col].astype(str)

    # kleine letters
    df[col] = df[col].str.lower()

    # Houd enkel nog woorden over
    df[col] = df[col].str.replace('[^A-z]', ' ')

    # stopwoorden verwijderen
    df[col] = df[col].apply(lambda x: ' '.join(x for x in x.split() if x not in stopwoorden_nl))

    # Lemmatization
    from textblob import Word
    df[col] = df[col].apply(lambda x: ' '.join([Word(x).lemmatize() for x in x.split()]))

    return df
