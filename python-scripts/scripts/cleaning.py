# # eerst topwoordenlijsten downloaden NOTE! dit doe je maar eenkeer
# import nltk
# from pyparsing import col
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


def multiToSingleSpace(df,c):
    '''Replaces all multy spaces for single space
    checks if any of the fields in a specific column has a double space
    if this is the case the loop will continue untill all doubles spaces
    are gone'''

    while df[c].str.find('  ').sum() > 0:
        df[c] = df[c].str.replace('  ', ' ')

    return df


# functie om stopworden te verwijderen
def schoonmaken(df, col):

    '''Deze functie schoont emails op door zoveel mogelijk overboodige teskt weg 
    te halen'''
    
    # kolommen omzetten naar string
    df[col] = df[col].astype(str)

    # het gaat hier om email berichten, veel voorkomende niks zeggende info kan 
    # weggelaten worden.
    df[col] = df[col].str.replace(r'(Geachte.{1,30}\n|Goedemiddag.{1,30}\n|Goedeavond.{1,30}\n|Beste.{1,20}\n)',' ')

    # alle line breaks omzetten naar ###
    df[col] = df[col].str.replace(r'\n',' ### ')
    df[col] = df[col].str.replace(r'(vriendelijke groet.*|mvg.*|kind regards.*)','')
    df[col] = df[col].str.replace(r'van:.*?verzonden:.*?aan:.*','')

    # alle ### weer terug zetten naar line breaks
    df[col] = df[col].str.replace(r' ### ','\n')

    # kleine letters
    df[col] = df[col].str.lower()

    # Houd enkel nog woorden over
    df[col] = df[col].str.replace('[^A-záéíóúýçäëïöüÿàèìòùâêîôûãõñ]', ' ')

    # Nederlandse stopworden inladen
    # from nltk.corpus import stopwords

    # stopwoorden_nl = stopwords.words('dutch')
    # stopwoorden verwijderen
    # df[col] = df[col].apply(lambda x: ' '.join(x for x in x.split() if x not in stopwoorden_nl))

    # Lemmatization
    # from textblob import Word
    # df[col] = df[col].apply(lambda x: ' '.join([Word(x).lemmatize() for x in x.split()]))

    return df



