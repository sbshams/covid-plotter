import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def get_country_data(countryName):
    script_dir = os.path.dirname(__file__)
    source_file = os.path.join(script_dir, '../covid-19/scripts/data/time-series-19-covid-combined.csv')

    # Getting data of specified country
    sourceData = pd.read_csv(source_file)
    countryData = sourceData[sourceData['Country/Region'] == countryName]
    countryData = countryData.dropna(axis = 1)
    countryData.rename(columns = {'Country/Region': 'Country' }, inplace=True)

    # Getting data ready for plot
    countryData = countryData.reset_index( drop = True )
    Index = countryData[countryData['Confirmed'] != 0].index.values
    dataFrame = countryData.iloc[ Index[0]-1 : Index[-1]+1 ]
    dataFrame = dataFrame.reset_index( drop = True )

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

    lastDate = dt.datetime.strptime( dataFrame['Date'].loc[dataFrame.last_valid_index()], '%Y-%m-%d' ).date()
    dateCol = []
    dateCol.append( lastDate + dt.timedelta(days=1) )

    countryName = []
    countryName.append( dataFrame['Country'].loc[dataFrame.last_valid_index()] )
    
    lat = []
    lat.append( dataFrame['Lat'].loc[dataFrame.last_valid_index()] )
    lon = []
    lon.append( dataFrame['Long'].loc[dataFrame.last_valid_index()] )

    dailyInc = []
    dailyInc.append( round(dataFrame['Daily Increase'].loc[dataFrame.last_valid_index()] * growthFacMean) )
    confirmedCases = []
    confirmedCases.append( dataFrame['Confirmed'].loc[dataFrame.last_valid_index()] + dailyInc[0] )
    incConst = []
    incConst.append( confirmedCases[0] / dataFrame['Confirmed'].loc[dataFrame.last_valid_index()] )

    recLst = []
    recLst.append( float( "NaN" ) )
    deathLst = []
    deathLst.append( float( "NaN" ) )
    
    growthConst = []
    growthConst.append(growthFacMean)
    
    i = 1
    while ( i < projectedNumDays ):
        dateCol.append( dateCol[i-1] + dt.timedelta(days=1)  )
        countryName.append( countryName[i-1] )
        lat.append( lat[i-1] )
        lon.append( lon[i-1] )

        dailyInc.append( round( dailyInc[i-1] * growthFacMean ) )
        confirmedCases.append( confirmedCases[i-1] + dailyInc[i] )
        incConst.append( confirmedCases[i] / confirmedCases[i-1] )

        recLst.append( float( "NaN" ) )
        growthConst.append( growthFacMean )
        i = i + 1
    
    deathLst = recLst.copy()

    catDict = {}
    catDict["Date"] = dateCol
    catDict["Country"] = countryName
    catDict["Lat"] = lat
    catDict["Long"] = lon
    catDict["Confirmed"] = confirmedCases
    catDict["Recovered"] = recLst
    catDict["Deaths"] = deathLst
    catDict["Daily Increase"] = dailyInc
    catDict["Increase Constant"] = incConst
    catDict["Growth Factor"] = growthConst

    catData = pd.DataFrame(catDict)
    dataFrame = pd.concat( [dataFrame, catData], ignore_index=True )
    return dataFrame


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
    
    countryName = str(dataFrame['Country'].loc[dataFrame.last_valid_index()])
    localPlotFilePath = 'saved_data/' + countryName + ' ' + str(dt.datetime.now().date()) + '.csv'
    dataFrame.to_csv(localPlotFilePath)

def save_estimated_data( dataFrame ):
    
    countryName = str(dataFrame['Country'].loc[dataFrame.last_valid_index()])
    localPlotFilePath = 'saved_data/' + countryName + ' EstData ' + str(dt.datetime.now().date()) + '.csv'
    dataFrame.to_csv(localPlotFilePath)

def main():
    pakData = get_country_data('India')
    pakData = add_daily_increase( pakData )
    pakData = get_increase_constant( pakData )
    pakData = get_growth_factor( pakData )

    growthFacMean = get_growth_factor_mean( pakData, 5 )
    mortalityRate = (pakData['Deaths'].loc[pakData.last_valid_index()] / pakData['Confirmed'].loc[pakData.last_valid_index()]) * 100
    
    print("\nAverage growth factor = ", growthFacMean)
    print("Mortality rate = ", mortalityRate)
    print()

    preEstIndex = pakData.last_valid_index()+1
    pakData = estimate_daily_increase( pakData, growthFacMean, 15)

    preData = pakData.iloc[ 0 : preEstIndex ]
    postData = pakData.iloc[ preEstIndex : pakData.last_valid_index()+1 ]
    
    estConfirmed = pakData['Confirmed'].loc[pakData.last_valid_index()]
    estDate = dt.datetime.strptime( str(pakData['Date'].loc[pakData.last_valid_index()]), '%Y-%m-%d' ).date()
    #estDate = dt.datetime.strftime('%Y-%m-%d')
    estDeaths = round( estConfirmed * (mortalityRate/100) )
    print("Estimated Confirmed Cases by", estDate," = ", estConfirmed )
    print("Estimated Deaths by", estDate, " = ", estDeaths)
    print()
    save_estimated_data(pakData)


    # Plotting the data
    fig, (ax1, ax2) = plt.subplots(2, 1)

    preData.plot(kind='line', use_index=True, y='Confirmed', ax=ax1, style='r', label='Current Cases')
    postData.plot(kind='line', use_index=True, y='Confirmed', ax=ax1, style='b--', label='Estimated Cases')
    ax1.set_xticklabels([])
    countryName = str(pakData['Country'].loc[pakData.last_valid_index()])
    ax1Title = 'Estimated Confirmed Cases of ' + countryName + ' by ' + str(estDate)
    ax1.set_title(ax1Title)

    preData.plot(kind='bar', use_index=True, y='Daily Increase', ax=ax2, label='Current Cases', color='r')
    ax2.set_xticklabels([])
    curDate = dt.datetime.strptime( str(preData['Date'].loc[preData.last_valid_index()]), '%Y-%m-%d' ).date()
    ax2Title = "Daily Increase till " + str(curDate)
    ax2.set_title(ax2Title)

    fig.subplots_adjust(hspace=0.5)

    plt.show()

if __name__== "__main__":
    main()
    
    
