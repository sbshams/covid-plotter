import os
import csv
#import pandas as pd

script_dir = os.path.dirname(__file__)
source_file = os.path.join(script_dir, '../covid-19/scripts/data/time-series-19-covid-combined.csv')

countryName = 'Pakistan'
localFilePath = 'separated_files/' + countryName + '.csv'

with open(source_file, 'r') as file, open(localFilePath, 'w', newline='') as file_out:
	reader = csv.reader(file)
	writer = csv.writer(file_out)
	
	i = 0
	for row in reader:
		if (i == 0):
			writer.writerow(row)
		if (row[1] == countryName):
			writer.writerow(row)
		i = i + 1

			
filteredFilePath = 'filtered_data/' + countryName + '.csv'

with open(localFilePath, 'r') as file, open(filteredFilePath, 'w', newline='') as file_out:
	reader = csv.reader(file)
	writer = csv.writer(file_out)

	i = 0
	for row in reader:
		if (i == 0):
			writer.writerow(row)
		elif (row[5] > '0'):
			writer.writerow(row)
		i = i + 1



 
### Will be used for sanity checking if file has been written or not
#
# check if size of file is 0
#if os.stat(file_path).st_size == 0:
 #   print('File is empty')
#else:
 #   print('File is not empty')