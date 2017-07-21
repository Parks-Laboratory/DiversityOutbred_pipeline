USE Epistasis
	GO

IF EXISTS(
	SELECT * FROM sys.all_views
	WHERE name = 'DO_ALL_TRAITS')
	DROP VIEW dbo.DO_ALL_TRAITS
	GO

CREATE VIEW dbo.DO_ALL_TRAITS
AS
SELECT A.Trait,
		B.chr AS Chr1, 
		B.pos AS SNP1,
		B.rsID AS rsID1,
		C.chr AS Chr2, 
		C.pos AS SNP2,
		C.rsID AS rsID2,
		A.Pvalue 
FROM [Epistasis].[dbo].[DO] AS A
	inner join [DO].[dbo].[Genotype_Mapping] AS B
	ON A.SNP1 = B.marker 
		inner join [DO].[dbo].[Genotype_Mapping] AS C
		ON A.SNP2 = C.marker
