SELECT TOP (100) inc.unid, binnen.naam, [actie], verzoek, ad.naam
FROM [TOPDESK_SAAS].[dbo].[incident] inc
left join soortbinnenkomst binnen on binnen.unid = inc.soortbinnenkomstid
left join actiedoor ad on ad.unid = inc.operatorgroupid
where datumaangemeld >= '2021-01-01' and ad.naam = 'OL-STIP' and binnen.naam != 'Telefonisch'