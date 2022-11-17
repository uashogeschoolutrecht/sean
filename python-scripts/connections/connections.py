def connectDB(db): 
    
    '''This function is used to connect to the HU server. 
    Please provide a valid database name in order to connect'''

    import pymssql 
    connect = pymssql.connect(
        server=input('voeg servernaam in!'),
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

def readfileRD(projectname, csvfile):
    
    '''This function takes as input a project folder name and csvfilename
    from the SURF Research Drive to import a file. Note: file must be 
    csv and be located in the [projectname]/data_in/ directory.'''

    import os
    from os import path
    import sys
    #check if file exists with csv extension in research drive of user
    userRD = os.getlogin()
    location = r'/home/{}/researchdrive/M21033303_DenA (Projectfolder)/DA_Onderzoek/{}/data_in/{}.csv'.format(userRD, projectname, csvfile)
   
    if not path.exists(location):
        raise Exception("Csv file does not exist in the project directory data_in")
        return
    
    import pandas as pd
    #read in csvfile from location
    df = pd.read_csv(location, nrows = 2, sep = ',')

    return df