SELECT *, CONCAT(Allele1Forward, Allele2Forward) as 'APair' INTO [DO].[dbo].[CONCATPIVOT]
  FROM [DO].[dbo].[Genotype_Calls]

ALTER TABLE [DO].[dbo].[CONCATPIVOT]
	DROP COLUMN X, Y, GCScore, Allele1Forward, Allele2Forward

DELETE FROM [DO].[dbo].[CONCATPIVOT]
WHERE APair = 'NULLNULL'

DECLARE @DynamicPivotQuery AS NVARCHAR(MAX)
DECLARE @ColumnName AS NVARCHAR(MAX)
-- Get Distinct values of the PIVOT Column
 SELECT @ColumnName = ISNULL(@ColumnName + ',','') + QUOTENAME(SampleID)
	FROM (SELECT DISTINCT SampleID FROM [DO].[dbo].[CONCATPIVOT]) AS SID
--Prepare the PIVOT query using the dynamic query
SET @DynamicPivotQuery = 
   'SELECT SNPName, ' + @ColumnName + ' INTO [DO].[dbo].[OUTPUT1]
    FROM [DO].[dbo].[CONCATPIVOT]
    PIVOT(MAX(APair) 
          FOR SampleID IN (' + @ColumnName + ')) AS PVTTable'
--Execute the Dynamic Pivot Query
EXEC sp_executesql @DynamicPivotQuery

SELECT *  INTO [DO].[dbo].[OUTPUT2]
	FROM [DO].[dbo].[Genotype_Mapping]

ALTER TABLE [DO].[dbo].[OUTPUT2]
	DROP COLUMN cM, A1F, A2F, type, isMM, isUnique, isBiallelic, tier, seqA, seqB, haploChrM, haploChrY

SELECT chr as 'snp_chr', marker AS 'snp_id', rsID, pos AS 'snp_bp_mm10' INTO [DO].[dbo].[OUTPUT2E]
	FROM [DO].[dbo].[OUTPUT2]

SELECT * INTO [DO].[dbo].[Genotype_Calls_Plink_Format]
	FROM [DO].[dbo].[OUTPUT2E] t2 
	Inner Join [DO].[dbo].[OUTPUT1] t1 
		ON t1.SNPName = t2.snp_id

ALTER TABLE [DO].[dbo].[Genotype_Calls_Plink_Format]
	DROP COLUMN SNPName

drop table [DO].[dbo].[OUTPUT1]
drop table [DO].[dbo].[OUTPUT2]
drop table [DO].[dbo].[OUTPUT2E]
drop table [DO].[dbo].[CONCATPIVOT]