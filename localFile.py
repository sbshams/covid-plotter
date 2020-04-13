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

def add_daily_increase( dataFrame ):
    confirmedCases = dataFrame['Confirmed'].to_list()
    
    dailyIncrease = []

    i = 0
    for elem  in confirmedCases:
        if (i == 0):
            dailyIncrease.append(0)
        else:
            dailyIncrease.append(elem - confirmedCases[i-1])
        i = i + 1
    
    dataFrame['Daily Increase'] = dailyIncrease
    return dataFrame

def get_increase_constant ( dataFrame ):
    
    confirmedCases = dataFrame['Confirmed'].to_list()

    increaseConstant = []

    i = 0
    for elem in confirmedCases:
        if (i == 0):
            increaseConstant.append(0)
        else:
            if ((elem != 0) & (confirmedCases[i-1] != 0)):
                increaseConstant.append( elem/confirmedCases[i-1] )
            else:
                increaseConstant.append(0)
        i = i + 1
    
    dataFrame['Increase Constant'] = increaseConstant
    return dataFrame

def get_growth_factor ( dataFrame ):

    if 'Daily Increase' in dataFrame.columns:

        dailyIncrease = dataFrame['Daily Increase'].to_list()

        growthFactor = []

        i = 0
        for elem in dailyIncrease:
            if (i == 0):
                growthFactor.append(0)
            else:
                if ((elem != 0) & (dailyIncrease[i-1] != 0)):
                    growthFactor.append( elem/dailyIncrease[i-1] )
                else:
                    growthFactor.append(0)
            i = i + 1
        
        dataFrame['Growth Factor'] = growthFactor
        return dataFrame
    else:
        print("Please get daily increase first! ")
        return dataFrame

def estimate_daily_increase( dataFrame, growthFacMean, projectedNumDays ):

    estDailyIncrease = []
    i = 0
    while ( i < projectedNumDays ):
        if (i == 0):
            estDailyIncrease.append( round(dataFrame['Daily Increase'].loc[dataFrame.last_valid_index()] * growthFacMean) )
        else:
            estDailyIncrease.append( round(estDailyIncrease[i-1] * growthFacMean) )
        i = i + 1
    
    estConfirmed = []
    i = 0
    while( i < projectedNumDays ):
        if ( i == 0 ):
            estConfirmed.append( dataFrame['Confirmed'].loc[dataFrame.last_valid_index()] + estDailyIncrease[i] )
        else:
            estConfirmed.append( estConfirmed[i-1] + estDailyIncrease[i] )
        i = i + 1
    
    print( estConfirmed )
    #dataFrame['Daily Increase'].append()


def get_increase_constant_mean( dataFrame, numDays):

    if (numDays <= (dataFrame.last_valid_index() - numDays)):    
        dataFrame = dataFrame.iloc[ dataFrame.last_valid_index() - numDays:dataFrame.last_valid_index() + 1 ]
        mean = dataFrame['Increase Constant'].mean()
    else:
        print("The number of Days is higher than the record value!")
        mean = dataFrame['Increase Constant'].mean()
    return mean

def get_growth_factor_mean( dataFrame, numDays):

    if (numDays <= (dataFrame.last_valid_index() - numDays)):    
        dataFrame = dataFrame.iloc[ dataFrame.last_valid_index() - numDays:dataFrame.last_valid_index() + 1 ]
        mean = dataFrame['Growth Factor'].mean()
    else:
        print("The number of Days is higher than the record value!")
        mean = dataFrame['Growth Factor'].mean()
    return mean

def save_data( dataFrame ):
    
    nameToCol = dataFrame['Country'].to_list()
    countryName = nameToCol[1]
    localPlotFilePath = 'saved_data/' + countryName + '.csv'
    dataFrame.to_csv(localPlotFilePath)


def main():
    pakData = get_country_data('Pakistan')
    pakData = add_daily_increase( pakData )
    pakData = get_increase_constant( pakData )
    pakData = get_growth_factor( pakData )

    growthFacMean = get_growth_factor_mean( pakData, 6 )
    print(growthFacMean)

    estimate_daily_increase( pakData, growthFacMean, 15)

    ax = plt.gca()
    pakData.plot(kind='bar',y='Daily Increase',ax=ax)
    ax.set_xticklabels([])
    #bangData.plot(kind='line',y='Confirmed',ax=ax, label = 'Bangladesh')
    #iranData.plot(kind='line',y='Confirmed',ax=ax, label = 'Iran')
    #indiaData.plot(kind='line',y='Confirmed',ax=ax, label = 'India')
    plt.title('Plot to show daily increase')
    #plt.show()
  
    save_data(pakData)

if __name__== "__main__":
    main()
    
    