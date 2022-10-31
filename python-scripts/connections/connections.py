def connectDB(db): 
    
    '''This function is used to connect to the HU server. 
    Please provide a valid database name in order to connect'''

    import pymssql 
    connect = pymssql.connect(
        server='DBND25.medewerkers.ad.hvu.nl',
        database=db)

    return connect

def sqlFileToString(sqlname):

    ''' Deze definitie leest sql bestanden in en zet ze vervolgens om 
    naar een string variabele die als input gebruikt kan worden voor
    het inlezen vanuit de database'''

    import re
    # sql locatie definieren
    file = r'./connections/sqls/{}.sql'.format(sqlname)

    # sql openen en opslaan in f
    f = open(file, 'r')

    # sql script inlezen
    sql = f.read()

    # beetje schoonmaken
    sql = re.sub('(\n|\r|\t)', ' ',sql)

    return sql