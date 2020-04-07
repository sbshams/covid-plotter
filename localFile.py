import os
import csv

script_dir = os.path.dirname(__file__)
source_file = os.path.join(script_dir, '../covid-19/scripts/data/time-series-19-covid-combined.csv')

with open(source_file, 'r') as file:
	reader = csv.reader(file)
	i = 0
	for row in reader:
		print(row)
		i = i + 1
		if(i>3):
			break

