/* Concatenates the A1lele columns to form a pair, optional replace(x, char1, char2) to remove spaces */
SELECT *, CONCAT(Allele1Forward, Allele2Forward) as 'APair' INTO [DO].[dbo].[CONCATPIVOT]
  FROM [DO].[dbo].[Genotype_Calls]

/* delete columns from the concat-ed table so that they won't be implicitly grouped by to form duplicate pivot rows */
ALTER TABLE [DO].[dbo].[CONCATPIVOT]
	DROP COLUMN X, Y, GCScore, Allele1Forward, Allele2Forward

/* Delete null column if the concat-ed pair is NULL, might result in missing SNPName rows if all sampleIDs are NULL*/
DELETE FROM [DO].[dbo].[CONCATPIVOT]
WHERE APair = 'NULLNULL'

/* Construct Dynamic Pivot Query by dynamically building @columnname */
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

/* We want to alter the format of Genotype_Mapping to prepare it for the inner join */
SELECT *  INTO [DO].[dbo].[OUTPUT2]
	FROM [DO].[dbo].[Genotype_Mapping]

/* Delete all unwanted columns */
ALTER TABLE [DO].[dbo].[OUTPUT2]
	DROP COLUMN cM, A1F, A2F, type, isMM, isUnique, isBiallelic, tier, seqA, seqB, haploChrM, haploChrY

/* Change the names. Can use sp_rename instead but might run into unknown conversion/naming errors */
SELECT chr as 'snp_chr', marker AS 'snp_id', rsID, pos AS 'snp_bp_mm10' INTO [DO].[dbo].[OUTPUT2E]
	FROM [DO].[dbo].[OUTPUT2]

/* Do inner join on the SNPName(primary key name for Genotype_calls) and snp_id (p.key name for G_mapping table) with cleaned up tables */
SELECT * INTO [DO].[dbo].[Genotype_Calls_Plink_Format]
	FROM [DO].[dbo].[OUTPUT2E] t2 
	Inner Join [DO].[dbo].[OUTPUT1] t1 
		ON t1.SNPName = t2.snp_id

/* After inner join remove the duplicate SNPName Column */
ALTER TABLE [DO].[dbo].[Genotype_Calls_Plink_Format]
	DROP COLUMN SNPName

/* Delete all intermittent tables */
drop table [DO].[dbo].[OUTPUT1]
drop table [DO].[dbo].[OUTPUT2]
drop table [DO].[dbo].[OUTPUT2E]
drop table [DO].[dbo].[CONCATPIVOT]