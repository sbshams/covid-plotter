import os
import pandas as pd
import numpy as np


# Country specifics for source data
countryName = 'Pakistan'
script_dir = os.path.dirname(__file__)
source_file = os.path.join(script_dir, '../covid-19/scripts/data/time-series-19-covid-combined.csv')
localFilePath = 'separated_files/' + countryName + '.csv'
localPlotFilePath = 'plot_files/' + countryName + '.csv'

# Getting data of specified country
sourceData = pd.read_csv(source_file)
countryData = sourceData[sourceData['Country/Region'] == countryName]
countryData = countryData.dropna(axis = 1)
countryData.rename(columns = {'Country/Region': 'Country' }, inplace=True)
countryData.to_csv(localFilePath)

# Getting data ready for plot
countryData = countryData.reset_index( drop = True )
Index = countryData[countryData['Confirmed'] != 0].index.values
plotData = countryData.iloc[ Index[0]-1 : Index[-1]+1 ]
plotData = plotData.reset_index( drop = True )
plotData.to_csv(localPlotFilePath)
