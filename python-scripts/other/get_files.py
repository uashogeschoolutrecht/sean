def loadTable():
    import pandas as pd
    from connections.connections import connectDB

    # connectie maken met database (default is nu op 25)
    conn = connectDB(db='TOPDESK_SAAS')

    from connections.connections import sqlFileToString
    # sql bestand inladen en omzetten naar string
    sql = sqlFileToString('topdesk_sample')

    # sql inladen en omzetten naar dataframe
    import warnings
    warnings.filterwarnings('ignore')
    bev_df = pd.read_sql_query(sql, conn)

    # connectie aflsuiten
    conn.close()

    # file zonder id voor anayse 
    df = pd.DataFrame(bev_df[[
        'melding',
        'verzoek',
        'actie',
        'ref_domein',
        'ref_specificatie'
        ]])

    # opschonen van bestand
    df['verzoek'] = df['verzoek'].str.lower()

    # bekijk de lengte van elk verzoek
    df['len_verzoek'] = df['verzoek'].str.len()

    # tel aantal email berichten aan de hand van de keren dat het woord onderwerp: voorkomt
    df['onderwerp_count'] = df['verzoek'].str.count(r'(onderwerp:|subject:)')

    # lengte van de spit
    split_len = max(df['onderwerp_count'])

    # aantal kolommen uitbreiden met max aantal keer dat onderwerp voorkomt
    cols = list()
    for i in range(split_len):
        cols += ['onderwerp_{}'.format(i)]
        

    # onderwerp teksten als aparte kolommen toevoegen
    df[cols] = df['verzoek'].str.split('onderwerp:', expand=True)

    # eerste uitbreiding weggooien bevat alleen infor van voor het woord onderwerp
    df.drop(columns='onderwerp_0', inplace=True)

    # onderwerp 0 uit cols list halen
    cols = cols[1:]

    # zoveel mogelijk troep weggooien voor elke kolom
    from other.cleaning import schoonmaken
    for c in cols:
        # eerst alle line braks omzetten naar ###
        df[c] = df[c].str.replace(r'\n',' ### ')
        df[c] = df[c].str.replace(r'(vriendelijke groet.*|mvg.*|kind regards.*)','')
        df[c] = df[c].str.replace(r'van:.*?verzonden:.*?aan:.*','')
        df[c] = df[c].str.replace(r' ### ','\n')

        # cijfer en andere tekens verwijderen, stopwoorden verwijderen
        df = schoonmaken(df,c)
        df[c] = df[c].str.replace('None','')

    # index ressetten voor de zekerheid
    df.reset_index(inplace=True, drop=True)

    return df

