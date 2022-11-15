SELECT TOP (500) inc.unid AS id
	,srt.naam AS melding
	,[actie]
	,verzoek 
	,ref_domein
	,ref_specificatie
FROM [dbo].[incident] AS inc
LEFT JOIN soortbinnenkomst AS srt ON srt.unid = inc.soortbinnenkomstid
LEFT JOIN actiedoor ad ON ad.unid = inc.operatorgroupid
WHERE datumaangemeld >= '2021-01-01'
	AND ad.naam = 'OL-STIP'
	AND srt.naam = 'E-Mail';


