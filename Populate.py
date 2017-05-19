import pyodbc
import csv
import os
from functools import reduce
import argparse

# Create parser to receive instructions from command line
parser = argparse.ArgumentParser(description = 'Input arguments to populate database')
# Argument to create table and whether to create new table
parser.add_argument('-t', '--tablename', action = 'store', help = "Table for inserting data", default = "Genotype_Calls")
parser.add_argument('-c', '--create', action = 'store_true', help = "Create table", default= False) 
# Argument to specify path
parser.add_argument('-p', '--path', action = 'store', help = "Directory path with txt file", default="E:/DO\ QTL\ MAPPING/GENOTYPES/Wave1")
# Argument to specify database
parser.add_argument('-db', '--database', action = 'store', help="Database to be opened", default = "DO")
# Parse all the the arguments together
args = parser.parse_args()
# Tokenize each argument into variables
tablename = args.tablename
create = args.create
path = args.path
database = args.database

# method to create table if needed
def createTable(database, tablename):
	global cursor
	
	query = "create table {!s} ".format(tablename) + "(" + \
			" SNPName varchar(50)," \
			" SampleID varchar(20)," \
			" Allele1Forward char(4)," \
			" Allele2Forward char(4)," \
			" X float," \
			" Y float," \
			" GCScore float,"\
			" CONSTRAINT ID PRIMARY KEY (SNPName, SampleID));"
	
	cursor.execute(query)
	cursor.commit()
	print("table %s successfully created in database %s" %(tablename, database))

# method to connect to the database
def createConnection(server, database):
	cn = pyodbc.connect('DRIVER={SQL Server}' + \
						';SERVER=' + server + \
						';DATABASE=' + database + \
						';Trusted_Connection= Yes')
	return cn

# "main" method which calls the functions and reads the txt file
if __name__ == '__main__':

	print("E:/DO\ QTL\ MAPPING/GENOTYPES/Wave1")
	print("There are whitespaces so escape keys are used as above, change the Wave directory after GENOTYPES")

	# connect to database
	cnxn = createConnection('PARKSLAB', database)
	print('connected to the database: %s successfully!' %database)
	cursor = cnxn.cursor()

	# if create is specified in the command line
	if create:
		createTable(database, tablename)

	# check if path exists
	if not os.path.isdir(path):
   		print('path does not exist')
		exit(1)

    # change directory
	os.chdir(path)

	fileNames = []

	# for each of the files in the dir ending with txt, add to the list
	for file in os.listdir(path):
		if file.endswith(".txt"):
			fileNames.append(file)

	for fileName in fileNames:

		print("Reading from:" + str(fileName))

		counter = 0

		with open(fileName, 'r') as txtFile:

			txtReader = csv.reader(txtFile, delimiter = '\t')

		# Looks for the index of '[Data]' line
			found = False
			for row in txtReader:

				for txt in row:

					if txt == '[Data]':
						found = True

				if found == True:
					break		

			# Skip through the description header after the [Data] section 
			fileFormat = next(txtReader)

			# Parse through the description header to get column number for database population 
			for cols in fileFormat:

				if cols == 'SNP Name':
					SNPNI = counter
				elif cols == 'Sample ID':
					SIDI = counter
				elif cols == 'Allele1 - Forward':
					A1FI = counter
				elif cols == 'Allele2 - Forward':
					A2FI = counter
				elif cols == 'X':
					XI = counter
				elif cols == 'Y':
					YI = counter
				elif cols == 'GC Score':
					GCSI = counter

				counter = counter + 1	

			index = 0
			# Resort each row to resemble the database format
			for rows in txtReader:

				index = index + 1

				list = [rows[SNPNI], rows[SIDI], rows[A1FI], rows[A2FI], rows[XI], rows[YI], rows[GCSI]]

				for i in range(0, len(list)):
					if list[i] == '-':
						list[i] = 'NULL'
					elif list[i] == 'NaN':
						list[i] == '0'	

				try:
					query = "insert into dbo.{!s}".format(tablename) +\
							"(SNPName, SampleID, Allele1Forward, Allele2Forward, X, Y, GCScore)" +\
							" values ({!r}, {!r}, {!r}, {!r}, {:.3f}, {:.3f}, {:.4f});".format(list[0], list[1], list[2], list[3], float(list[4]), float(list[5]), float(list[6]))
					cursor.execute(query)
					cursor.commit()

				
				# write errmsg if file I/O exception
				except ValueError as ex:

					errmsg = "Warning: Value Error in " + str(fileName) + ", primary key is: {!r}, {!r}".format(list[0], list[1]) + ", the line is: " + str(counter)
					f = open("GC_{!r}_err.txt".format(tablename), "w")
					f.write(errmsg + "\n")
					f.write(list)
					f.close()

				except IndexError as iex :
					errmsg = "Warning: Index error in " + str(fileName) + ", primary key is: {!r}, {!r}".format(list[0], list[1])
					f = open("GC_{!r}_err.txt".format(tablename), "w")
					f.write(errmsg + "\n")
					f.write(list)
					f.close()

				except Exception as eex:
					print("Primary Key Integrity Violation for insert #" + str(index))

				else:
					print("Insert " + str(index) + " was successful!")

	cursor.commit()
	print("File Read Done!" + str(fileName))
	cnxn.close()	