import pyodbc
import csv
import os
from functools import reduce
import argparse

# Create parser to receive instructions from command line
parser = argparse.ArgumentParser(description = 'Input arguments to populate database')
# Argument to create table and whether to create new table
parser.add_argument('-t', '--tablename', action = 'store', help = "Table for inserting data", default = "Genotype_Mapping")
parser.add_argument('-c', '--create', action = 'store_true', help = "Create table", default= False) 
# Argument to specify path
parser.add_argument('-p', '--path', action = 'store', help = "Directory path with txt file", default="E:/DO QTL MAPPING/")
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
			"marker varchar(40)," \
			" chr char(4)," \
			" pos float," \
			" cM float," \
			" A1F char(4)," \
			" A2F char(4)," \
			" type char(40)," \
			" isMM char(5),"\
			" isUnique char(5),"\
			" isBiallelic char(5),"\
			" tier char(4),"\
			" rsID varchar(40),"\
			" seqA varchar(max),"\
			" seqB varchar(max),"\
			" haploChrM char(5),"\
			" haploChrY char(5),"\
			" CONSTRAINT MapID PRIMARY KEY (marker));"
	print(query)
	
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

	print('E:/DO\ QTL\ MAPPING/')
	print("Input the above path since we need to use escape characters")

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

			# Skip through the description header after the [Data] section 
			fileFormat = next(txtReader)

			index = 0
			# Resort each row to resemble the database format
			for rows in txtReader:

				index = index + 1

				list = []

				for cols in rows[1:]:

					list.append(cols)
				
				for i in range(0, len(list)):
					if list[i] == 'NA':
						list[i] = 'NULL'
	
				# Converts pos to raw number instead of in millions
				list[2] = float(list[2])*1000000

				try:
					if list[3] != 'NULL': 

						query = "insert into dbo.{!s}".format(tablename) +\
								"(marker, chr, pos, cM, A1F, A2F, type, isMM, isUnique, isBiallelic, tier, rsID, seqA,seqB, haploChrM, haploChrY)" + \
								" values ({!r}, {!r}, {:d}, {:.13f}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r});".format(list[0], list[1], int(list[2]), float(list[3]), list[4], list[5], list[6], list[7], list[8], list[9], list[10], list[11], list[12], list[13], list[14], list[15])
						cursor.execute(query)
						cursor.commit()
						
					else: 
						query = "insert into dbo.{!s}".format(tablename) +\
								"(marker, chr, pos, cM, A1F, A2F, type, isMM, isUnique, isBiallelic, tier, rsID, seqA,seqB, haploChrM, haploChrY)" + \
								" values ({!r}, {!r}, {:d}, ?, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r});".format(list[0], list[1], int(list[2]), list[4], list[5], list[6], list[7], list[8], list[9], list[10], list[11], list[12], list[13], list[14], list[15])
						cursor.execute(query, None)
						cursor.commit()

				
				# write errmsg if file I/O exception
				except ValueError as ex:

					errmsg = "Warning: Value Error in " + str(fileName) + ", primary key is: {!r}".format(list[0]) + ", the line is: " + str(counter)
					f = open("GC_{!r}_err.txt".format(tablename), "w")
					f.write(errmsg + "\n")
					f.write(str(list))
					f.close()

				except IndexError as iex :
					errmsg = "Warning: Index error in " + str(fileName) + ", primary key is: {!r}, {!r}".format(list[0], list[1])
					f = open("GC_{!r}_err.txt".format(tablename), "w")
					f.write(errmsg + "\n")
					f.write(str(list))
					f.close()

				except Exception as eex:
					print("Primary Key Integrity Violation for insert #" + str(index))

				else:
					print("Insert " + str(index) + " was successful!")
	
	cursor.commit()
	print("File Read Done!" + str(fileName))
	cnxn.close()
						