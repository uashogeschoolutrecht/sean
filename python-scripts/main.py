#################################################################################
# Titel         : "Sean: the HU sentimenent analysis algorithm"
# Auteur        : Anne Leemans
# Start datum   : 27/10/2022
# Python versie : Python 3.10.7
#################################################################################

######################### SENTIMENT O.B.V. VERZOEK KOLOM #########################
if __name__ == "__main__":
    from scripts.getdata import loadTable

    # data inladen 
    clean_data = loadTable(colum='verzoek')
    df = clean_data.copy()

    # Boolean model halen
    from scripts.sentiment import sentimetBoolean
    df_sent_bool = sentimetBoolean(df,0.95, 'onderwerp_1')

    # Likert scale model binnen halen
    from scripts.sentiment import sentimetLikert
    df_sent_likert = sentimetLikert(df, 'onderwerp_1')

    # data prepareren voor visualisatie
    from scripts.visualize import sentimentVisDfBool,sentimentVisDfLikert
    df_sent_bool_vis = sentimentVisDfBool(df_sent_bool, 'ref_specificatie')
    df_sent_likert_vis = sentimentVisDfLikert(df_sent_likert, 'ref_specificatie')

    # toon barplot
    from scripts.visualize import sentimentBarPlotBool,sentimentBarPlotLikert
    sentimentBarPlotBool(df_sent_bool_vis.head(15),'Sentiment van eerste vraag uit verzoek emails naar referentie Boolean   \n')
    sentimentBarPlotLikert(df_sent_likert_vis.head(15),'Sentiment van eerste vraag uit verzoek emails naar referentie Likert   \n')
