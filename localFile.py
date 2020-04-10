import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_country_data(countryName):
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
    dataFrame = countryData.iloc[ Index[0]-1 : Index[-1]+1 ]
    dataFrame = dataFrame.reset_index( drop = True )
    dataFrame.to_csv(localPlotFilePath)

    return dataFrame


def main():
    pakData = get_country_data('Pakistan')
    bangData = get_country_data('Bangladesh')
    iranData = get_country_data('Iran')
    indiaData = get_country_data('India')

    ax = plt.gca()

    pakData.plot(kind='line',y='Confirmed',ax=ax, label = 'Pakistan')
    bangData.plot(kind='line',y='Confirmed',ax=ax, label = 'Bangladesh')
    iranData.plot(kind='line',y='Confirmed',ax=ax, label = 'Iran')
    indiaData.plot(kind='line',y='Confirmed',ax=ax, label = 'India')
    plt.title('Confirmed Cases Plot')
    plt.show()
  
if __name__== "__main__":
  main()
    
    