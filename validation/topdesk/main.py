if __name__ == "__main__":

    # set  input columns, 
    colname = 'verzoek'

    from readfiles import getDfFromDB
    # read topdesk data from database
    topdesk_df = getDfFromDB(
        db='TOPDESK_SAAS',
        sql='''SELECT TOP (500) CONVERT(VARCHAR(256), inc.unid) AS id
                ,srt.naam AS melding
                ,{}
                ,ref_domein
                ,ref_specificatie
            FROM [dbo].[incident] AS inc
            LEFT JOIN soortbinnenkomst AS srt ON srt.unid = inc.soortbinnenkomstid
            LEFT JOIN actiedoor ad ON ad.unid = inc.operatorgroupid
            WHERE datumaangemeld >= '2021-01-01'
                AND ad.naam = 'OL-STIP'
                AND srt.naam = 'E-Mail';'''.format(colname)
    )

    # clean emails
    from readfiles import emailThreadToEmails
    emails_df = emailThreadToEmails(topdesk_df[['id',colname]])

    # merge back together
    topdesk_df = topdesk_df.merge(emails_df,'left')

    # save to csv for further analysis   
    emails_df.to_csv(r'user-app\input\topdeskemails.csv', sep=';',encoding='utf-8-sig', encoding=True)






