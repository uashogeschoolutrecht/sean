def connectDB(db):     
    '''This function is used to connect to the HU server. 
    Please provide a valid database name in order to connect'''
    import pymssql 
    connect = pymssql.connect(
        server=input('voeg servernaam in!'),
        database=db)

    return connect

def getDfFromDB(db,sql):
    import pandas as pd
    # connectie maken met database (default is nu op 25)
    conn = connectDB(db=db)

    import warnings
    warnings.filterwarnings('ignore')
    df = pd.read_sql_query(sql, conn)

    # connectie aflsuiten
    conn.close()

    return df

def cleanEmails(dtframe, colname):
    '''Removes redundent info from email text'''

    # copy of dataframe for cleaning
    df = dtframe.copy()
    
    # kolommen omzetten naar string
    df[colname] = df[colname].astype(str)

    # all text to lower case
    df[colname] = df[colname].str.lower()

    # all text from start of email can be removed
    df[colname] = df[colname].str.replace(r'(geachte.{1,30}\n|goedemiddag.{1,30}\n|goedemorgen.{1,30}\n|goedeavond.{1,30}\n|beste.{1,20}\n)',' ')

    # all line breaks to  ###
    df[colname] = df[colname].str.replace(r'\n',' ### ')

    # remove all after 
    df[colname] = df[colname].str.replace(r'(vriendelijke groet.*|mvg.*|kind regards.*)','')

    # remove all info at start
    df[colname] = df[colname].str.replace(r'van:.*?verzonden:.*?aan:.*','')

    # remove all emails from text
    df[colname] = df[colname].str.replace(r'(.{1,20}@,{1,20}\.[a-z]{2,4})','')

    # all ### back to linebreaks
    df[colname] = df[colname].str.replace(r' ### ','\n')

    return df

def emailThreadToEmails(dtframe,seperator=r'Onderwerp:.*?\n'):
    '''This defenition transforms emai thread to seperate email mesagges en removes al 
    redundant text. The use can define a seperater depending on the type of thread. 
    Regex is accepted. 
    NOTE! only dataframes with two columns are accepted ['id', 'email] <-- columns'''

    # check if dataframe had only two columns
    if len(dtframe.columns) != 2:
        raise Exception('data frame has to many columns, make sure you use format: ["id","email"]')
    
    df = dtframe.copy()
    
    # always take second column name for input
    colname = list(df)[1]
    
    # count emails in thread
    df['email_count'] = df[colname].str.count(seperator)
    df['len'] = df[colname].str.len()

        
    # define the length of the split based on the max amount of email in one thread
    split_len = int(max(df['email_count']))

    # set the amount of columns 
    cols = list()
    for i in range(split_len+1):
        cols += ['email_{}'.format(i)]
    
    # split columns on seperator 
    df[cols] = df[colname].str.split(seperator, expand=True)
    dropcols = ['email_count', 'email_0']

    # eerste uitbreiding weggooien bevat alleen info van voor het woord onderwerp onderwerp count is ook niet meer nodig
    df.drop(columns=dropcols, inplace=True)

    # clean email columns
    for c in cols[1:]:
        df = cleanEmails(df,c)

    # return id and email columns
    df = df[[df.columns[0]]+ cols[1:]]

    return df

