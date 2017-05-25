# Genomic Database Dataset Importing and Table Joining
This project includes Python and SQL code. The python files are used to import tab delimited datasets from
.txt files. Two separate tables were created and populated based on differing raw schemas which were observed 
from the datasets (examples can be found in the repository). An SQL Script was then used to merge the tables
into a single pivoted table that can be understood by Plink. The rest of the queries are then used to debug
the pivot table to check for duplicates and missing values. 

## 1. Usage 
Run the following linux command on a server with the python package pre-installed on it.
```
python (Python File) (Table Name) (Create Table) (File Path) (SQL Database)
```
Function: Populating a table in the SQL Database from datasets stored in a .txt file in a file path  
Python File: Populate.py / Populate_mapping.py    
Table Name: name of the table we want to populate or create   
Create Table: -c flag to create table, the default is no   
File Path: File path that the .txt files can be read from   
SQL Database: Name of SQL Database in SQL Server  

### Example 
#### Populate.py 
```
python Populate.py -t Genotype_Calls -c -p E:/DO\ QTL\ MAPPING/ -db DO
```
The python program will create a new table in the DO database in SQL Server called Genotype_Calls by parsing through 
.txt files in the -p specified directory.

However for Populate.py, only .txt files delimited by tabs like "Genotype Calls Dataset.txt" in the repo would work
which is formatted like below: 
```
[Header]
GSGT Version	1.9.4
Processing Date	11/17/2016 2:38 PM
Content		GigaMuga_11769261_A.bpm
Num SNPs	143259
Total SNPs	143446
Num Samples	5
Total Samples	5
[Data]
SNP Name	Sample ID	Allele1 - Forward	Allele2 - Forward	X	Y	GC Score	Theta	X Raw	Y Raw	R
AmpR002	DO357	T	T	3.727	0.263	0.4204	0.045	10987	1186	3.990
B6_01-011986786-S	DO357	C	C	0.000	0.599	0.8734	1.000	202	1780	0.599
B6_01-033811444-S	DO357	T	T	0.057	0.774	0.9233	0.953	500	2045	0.831
B6_01-074963079-S	DO357	C	C	0.115	0.889	0.4894	0.918	571	2605	1.004
```
Populate.py skips through the header until it detect a [Data] row and then skips through the next header in [Data] and populates
the database with SNPName, SampleID, Allele1-Forward, Allele2Forward, X, Y, GCScore. It does not matter if the header's order
are jumbled up since it detects the order of the string, parses and loads it into the database. Composite primary keys are 
built on (SNPName, SampleID)

#### Populate_mapping.py
The command line argument is run similar to the one above but we change the .py file name
For the .txt file formats, the format differs from the dataset used to populate the Genotype_Calls table and is included in "Mapping Dataset.txt" and the format is shown below:
```
"marker"  "chr" "pos"	"cM"  "A1"	"A2"	"type"	"is.MM"	"unique"	"is.biallelic"	"tier"	"rsID"	"seq.A"	"seq.B"	"haploChrM"	"haploChrY"
"UNC16386"	"UNC16386"	"1"	4.446737	0.0663498428074156	"A"	"G"	"haplotype_discrimination"	TRUE	TRUE	TRUE	1	"rs51852623"	"ACCTGTAGACAGCATGCAGTTGAGTATTAGATTCACTCAGTCATTGTCTG"	NA	FALSE	FALSE
"UNCHS000017"	"UNCHS000017"	"1"	4.498713	0.0667535936246036	"C"	"A"	"recomb_hotspot"	FALSE	TRUE	TRUE	1	"rs214452121"	"GTATGTGCATCTTCAGCCTGGCTTTCTTCGATAAAAGCATTAAGATAGCC"	NA	FALSE	FALSE
"UNCHS000018"	"UNCHS000018"	"1"	4.504223	0.0667963954370306	"G"	"A"	"recomb_hotspot"	FALSE	TRUE	TRUE	1	"rs231202172"	"AAGAACACACCACACACCATAGATAAATATTAAATAAAGAAGAACACAGA"	NA	FALSE	FALSE
```
Populate_mapping.py skip through the header and parses through all the attributes found in the header. The primary key "marker"
refers to the SNPName in the composite key in populate.py.

#### SQL Plink Conversion.sql
This SQL script is built using a dynamic SQL query. It builds a pivot table of SampleIDs based on marker or SNPName AKA 'snp_id'
by joining similar snp_id's on the Genotype_Calls and Genotype_mapping table.
```
snp_chr	snp_id	rsID	snp_bp_mm10	DO294	DO540	DO101	DO045	DO111	DO301	DO463	DO519	DO539	DO156	DO230	DO239	DO206	DO555	DO150	DO529	DO500	DO136	DO373	DO375	DO152	DO303	DO269	DO355	DO511	DO184	DO021	DO364	DO129	GC001	DO109	DO285	DO063	DO315	DO471	DO171	DO222	DO258	DO271	DO349	DO168	DO404	DO030	DO095	DO194	DO339	DO391	DO494	DO413	DO252	DO320	DO496	DO072	DO081	DO144	DO411	DO090	DO383	DO235	DO242	DO070	DO106	DO378	DO137	DO541	DO257	DO114	DO120	DO518	DO282	DO505	DO530	DO092	DO040	DO155	DO522	DO547	DO556	DO053	DO061	DO210	DO358	DO516	DO118	DO376	DO108	DO288	DO388	DO553	DO059	DO172	DO248	DO497	DO369	DO468	DO147	DO507	DO085	DO191	DO262	DO327	DO334	DO024	DO363	DO309	DO410	DO197	DO321	DO396	DO029	DO401	DO185	DO295	DO318	DO274	DO141	DO143	DO031	DO098	DO338	DO394	DO406	DO483	DO499	DO161	DO380	DO403	DO179	DO200	DO237	DO267	DO236	DO537	DO359	DO207	DO038	DO113	DO158	DO546	DO166	DO419	DO067	DO121	DO279	DO093	DO361	DO377	DO531	DO043	DO127	DO469	DO504	DO508	TC001	DO049	DO054	DO213	DO521	DO353	DO305	DO220	DO247	DO533	DO550	DO065	DO134	DO350	DO341	DO492	DO023	DO362	DO088	DO265	DO287	DO331	DO074	DO032	DO164	DO217	DO385	DO028	DO123	DO180	DO196	DO397	DO368	DO319	DO407	DO486	DO186	DO254	DO326	DO126	DO244	DO418	DO110	DO203	DO558	DO306	DO039	DO100	DO231	DO051	DO212	DO276	DO399	DO466	DO233	DO524	DO370	DO079	DO300	DO302	DO503	DO510	DO356	DO536	DO367	DO181	DO260	DO495	DO060	DO476	DO057	DO170	DO221	DO223	DO330	DO336	DO062	DO478	DO116	DO227	DO310	DO026	DO149	DO259	DO187	DO272	DO297	DO344	DO348	DO169	DO416	DO485	DO071	DO096	DO199	DO251	DO253	DO392	DO084	DO405	DO033	DO408	DO243	DO379	DO047	DO215	DO461	DO103	DO138	DO209	DO234	DO395	DO517	DO202	DO417	DO420	DO277	DO346	DO542	DO559	DO069	DO115	DO523	DO052	DO467	DO506	DO281	DO557	DO076	DO513	DO117	DO154	DO351	DO357	DO132	DO371	DO086	DO175	DO263	DO409	DO372	DO107	DO389	DO475	DO099	DO333	DO058	DO226	DO311	DO190	DO360	DO241	DO322	DO146	DO415	DO317	DO343	DO544	DO290	DO034	DO097	DO083	DO177	DO162	DO188	DO219	DO387	DO275	DO296	DO480	DO324	DO044	DO291	DO178	DO400	DO464	DO066	DO112	DO122	DO124	DO157	CS001	DO102	DO139	DO545	DO205	DO238	DO473	DO512	DO308	DO313	DO532	DO528	DO268	DO520	DO135	DO501	DO534	DO048	DO055	DO214	DO354	DO560	DO035	DO332	DO340	DO414	DO087	DO089	DO264	DO526	DO064	DO193	DO284	DO365	DO470	DO316	DO255	DO398	DO145	DO167	DO487	DO488	DO493	DO165	DO189	DO218	DO384	DO073	DO325	DO390	DO183	DO382	DO082	DO412	DO078	DO250	DO292	DO232	DO465	DO125	DO245	DO148	DO204	DO041	DO119	DO472	DO527	DO307	DO050	DO283	DO502	DO548	DO525	DO211	DO552	DO130	DO535	DO328	DO482	DO498	SF001	DO140	DO515	DO182	DO366	DO192	DO477	DO479	DO173	DO261	DO289	DO025	DO228	DO484	DO142	DO256	DO345	DO056	DO224	DO347	DO489	DO105	DO198	DO337	DO393	DO249	DO273	DO298	DO036	DO160	DO381	DO402	DO462	DO037	DO104	HK001	DO176	DO201	DO208	DO151	DO543	ZF001	DO538	DO068	DO240	DO278	DO304	DO335	DO374	DO280	DO554	DO094	DO509	DO042	DO128	DO153	DO352	DO131	DO133	DO046	DO216	DO549	DO077	DO266	DO514	DO474	DO551	DO174	DO246	DO329	DO491	DO022	DO091	DO229	DO312	DO314	DO225	DO286	DO195	DO027	DO159	DO163	DO386	DO270	DO299	DO490	DO080	DO342	DO481	DO293	DO075	DO323
17  	backupJAX00442970	rs48941080	59883681	A   G   	G   G   	A   A   	A   G   	G   G   	A   G   	A   A   	G   G   	A   G   	G   G   	A   G   	A   G   	G   G   	A   G   	A   A   	G   G   	G   G   	G   G   	G   G   	G   G   	A   G   	G   G   	G   G   	G   G   	G   G   	G   G   	G   G   	A   G   	A   G   	G   G   	A   A   	A   G   	G   G   	G   G   	A   A   	A   G   	A   G   	G   G   	G   G   	G   G   	G   G   	G   G   	G   G   	A   G   	G   G   	G   G   	A   G   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	A   G   	A   G   	G   G   	A   A   	G   G   	A   G   	G   G   	G   G   	A   A   	A   G   	A   G   	A   G   	A   A   	A   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	A   A   	A   A   	G   G   	A   A   	A   G   	A   G   	A   G   	A   A   	G   G   	A   G   	A   G   	G   G   	A   G   	A   G   	G   G   	G   G   	G   G   	A   G   	A   A   	A   G   	A   A   	G   G   	G   G   	A   G   	A   G   	G   G   	A   A   	A   G   	G   G   	A   G   	A   A   	G   G   	G   G   	A   G   	G   G   	G   G   	A   A   	NULL	A   G   	A   G   	A   G   	A   G   	G   G   	A   G   	G   G   	A   G   	G   G   	G   G   	G   G   	A   G   	A   A   	A   A   	A   G   	A   A   	A   G   	G   G   	G   G   	A   A   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   A   	A   G   	A   G   	A   G   	A   G   	G   G   	A   A   	A   G   	A   A   	G   G   	A   G   	G   G   	A   A   	A   G   	NULL	A   G   	A   G   	A   A   	A   A   	G   G   	A   A   	A   G   	A   G   	A   G   	A   G   	G   G   	A   A   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	G   G   	A   A   	A   G   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	A   G   	A   G   	A   G   	G   G   	A   A   	A   G   	G   G   	A   G   	A   A   	G   G   	A   G   	A   A   	G   G   	G   G   	G   G   	A   A   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	A   G   	A   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	A   G   	A   G   	G   G   	A   G   	A   G   	G   G   	A   A   	A   A   	A   G   	A   G   	A   G   	A   G   	G   G   	A   A   	A   A   	G   G   	G   G   	NULL	A   G   	A   A   	G   G   	A   G   	A   G   	G   G   	G   G   	A   G   	A   A   	A   G   	A   G   	G   G   	G   G   	A   G   	A   G   	A   G   	G   G   	A   G   	G   G   	A   G   	G   G   	A   G   	A   G   	A   G   	G   G   	A   G   	G   G   	A   G   	G   G   	A   G   	A   G   	A   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	A   G   	G   G   	A   G   	A   A   	A   G   	A   A   	G   G   	A   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	A   A   	G   G   	A   G   	G   G   	G   G   	G   G   	G   G   	G   G   	A   A   	A   G   	A   A   	A   A   	A   A   	A   G   	A   G   	A   G   	A   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	G   G   	A   G   	G   G   	A   G   	A   G   	A   A   	A   G   	G   G   	A   G   	A   G   	A   G   	G   G   	G   G   	A   G   	A   A   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	G   G   	A   A   	G   G   	A   G   	A   G   	G   G   	G   G   	A   G   	G   G   	A   G   	G   G   	A   G   	NULL	G   G   	G   G   	A   G   	A   G   	NULL	G   G   	A   A   	A   G   	G   G   	A   G   	A   G   	G   G   	A   G   	A   G   	A   A   	A   G   	G   G   	G   G   	A   A   	G   G   	A   G   	G   G   	A   G   	A   G   	A   A   	G   G   	A   A   	A   A   	A   G   	G   G   	A   G   	A   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	A   G   	G   G   	A   G   	G   G   	A   G   	A   G   	G   G   	G   G   	A   G   	A   G   	A   A   	A   G   	G   G   	A   G   	G   G   	G   G   	A   G   	G   G   	G   G   	A   G   	G   G   	A   G   	G   G   	NULL	A   G   	A   G   	A   G   	G   G   	A   A   	G   G   	G   G   	A   G   	G   G   	A   A   	A   A   	G   G   	A   G   	A   G   	G   G   	G   G   	G   G   	G   G   	A   G   	A   G   	G   G   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	G   G   	A   A   	A   G   	A   G   	G   G   	G   G   	A   G   	A   G   	A   A   	A   G   	A   G   	G   G   	A   A   	A   G   	A   G   	G   G   	A   G   	A   A   	G   G   	A   G   	A   G   	A   G   	A   G   	A   G   	A   G   	G   G   	G   G   	G   G   	G   G   	A   G   	G   G   	G   G   	A   A   	A   G   	A   G   	A   G   	G   G   	A   G   	G   G   	G   G   	G   G   	A   G   	A   G   	A   G   	A   G   	A   A   	G   G   	G   G   	A   G   	A   G   	G   G   	G   G   	G   G   	A   A   	A   G   	A   G   	A   A   	A   G   	A   G   	A   A   	A   G   	A   G   
```
