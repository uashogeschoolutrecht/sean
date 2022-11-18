def readCsv(csvfile,sep=';',nrows=None):
    import os
    from os import path
    #check if file exists with csv extension in research drive of user
    userRD = os.getlogin()
    location = r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\user-app\input\{}.csv'.format(csvfile)
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