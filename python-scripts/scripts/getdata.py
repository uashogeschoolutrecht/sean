

def getDfFromDB(db,sql):
    import pandas as pd
    from connections.connections import connectDB

    # connectie maken met database (default is nu op 25)
    conn = connectDB(db=db)

    from connections.connections import sqlFileToString
    # sql bestand inladen en omzetten naar string
    sql = sqlFileToString(sql)

    # sql inladen en omzetten naar dataframe
    import warnings
    warnings.filterwarnings('ignore')
    df = pd.read_sql_query(sql, conn)

    # connectie aflsuiten
    conn.close()

    return df

# geschoonde data inladen
def loadTable(column):

    bev_df = getDfFromDB(db='TOPDESK_SAAS',sql='topdesk_sample')

    import pandas as pd
    # file zonder id voor anayse 
    df = pd.DataFrame(bev_df[[
        'melding',
        column,
        'ref_domein',
        'ref_specificatie'
        ]])
    
    # indien het gaat om een verzoek tel aantal email berichten aan de hand van de keren dat het woord onderwerp: voorkomt
    if column == 'verzoek':
        df['onderwerp_count'] = df[column].str.count(r'(Onderwerp:|Subject:)')
    else:
        df['onderwerp_count'] = df[column].str.count(r'([0-9]{2}-[0-9]{2}-[0-9]{4}|[0-9]{2}-[A-z]{3}-[0-9]{4})')*2

    # lengte van de spit
    split_len = max(df['onderwerp_count'])

    # aantal kolommen uitbreiden met max aantal keer dat onderwerp voorkomt
    cols = list()
    for i in range(split_len+1):
        cols += ['onderwerp_{}'.format(i)]
    
    # onderwerp teksten als aparte kolommen toevoegen
    if column == 'verzoek':
        cols = cols[:-1]
        df[cols] = df[column].str.split('Onderwerp:.*?\n', expand=True)
        dropcols = ['onderwerp_count', 'onderwerp_0']
    else:
        df[cols] = df[column].str.split(r'([0-9]{2}-[0-9]{2}-[0-9]{4}.*?\n|[0-9]{2}-[A-z]{3}-[0-9]{4}.*?\n)', expand=True)
        dropcols = ['onderwerp_count', 'onderwerp_0']
        for i in range(1,split_len+1,2):
            dropcols += ['onderwerp_{}'.format(i)]

    # eerste uitbreiding weggooien bevat alleen info van voor het woord onderwerp onderwerp count is ook niet meer nodig
    df.drop(columnns=dropcols, inplace=True)

    if column == 'actie':
        p = 2
        for i in range(1,int(split_len/2+1)):
            df.rename(columnns={'onderwerp_{}'.format(p):'onderwerp_{}'.format(i)},inplace=True)
            p += 2


    # voor versie 0.1 van SEAN kijken we alleen naar het eerst onderwerp
    df = df[df.columnns.to_list()[:5]]

    # onderwerp 0 uit cols list halen !NOTE bij meer onderwerpen nr 2 aanpassen
    cols = cols[1:2]

    # zoveel mogelijk troep weggooien voor elke kolom
    from scripts.cleaning import schoonmaken
    from scripts.cleaning import multiToSingleSpace

    for c in cols:
        # cijfer en andere tekens verwijderen
        df = schoonmaken(df,c)
        df = multiToSingleSpace(df,c)

    # lege oonderwerpen verwijderen 
    df = df[df['onderwerp_1']!=' ']

    # taal detecter om te bepalen welk woordenboek gebruikt moet worden
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0

    df['taal'] = df['onderwerp_1'].apply(lambda x: detect(x))

    # engelse reacties verwijderen !NOTE dit is voor SEAN 0.1 toekomst wellicht anders
    df = df[(df['taal']!='en')]
    df = df[(df['onderwerp_1']!='none')]

    # index resetten
    df.reset_index(drop=True, inplace=True)

    return df
