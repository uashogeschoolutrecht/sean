def readCsv(csvfile, project, sep=';',nrows=None):
    import os
    from os import path
    #check if file exists with csv extension in research drive of user
    userRD = os.getlogin()
    location = r'/home/{}/researchdrive/M21033303_DenA (Projectfolder)/DA_Onderzoek/{}/data_in/{}.csv'.format(userRD, project, csvfile)
    path.exists(location)

    if not path.exists(location):

        # if does not exist raise error 
        raise Exception("Csv file does not exist in the project directory data_in")

    else:
        import pandas as pd
        # else if read csvfile from location
        df = pd.read_csv(
            filepath_or_buffer=location,
            sep=sep,
            nrows=nrows
            )

        return df