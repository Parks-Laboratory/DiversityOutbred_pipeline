SELECT count(rsID), marker 
  FROM [DO].[dbo].[Genotype_Mapping]
  WHERE rsID IS NOT NULL
  GROUP BY marker
  HAVING 
	count(rsID) > 1
