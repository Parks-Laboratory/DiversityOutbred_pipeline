SELECT DISTINCT SNPName
FROM [DO].[dbo].[Genotype_Calls] t3
WHERE NOT EXISTS 
	(SELECT * 
		FROM (SELECT DISTINCT SNPName 
			FROM [DO].[dbo].[Genotype_Calls] t1
			INNER JOIN [DO].[dbo].[Genotype_Mapping] t2
			ON t1.SNPName = t2.marker) t4
		WHERE t3.SNPName = t4.SNPName)

