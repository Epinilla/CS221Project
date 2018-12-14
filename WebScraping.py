import pandas as pd
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

# from geekstogeeks.org
def convert24(str1):
    if len(str1) == 7:
        str1 = '0' + str1
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
    elif str1[-2:] == "AM":
        return str1[:-2]
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]

# Read the table
def getFields(url, planeTime):
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        chrome_driver_binary = '/Users/EmanuelPinilla/Downloads/CS221-PSETS/Project/chromedriver'
        driver = webdriver.Chrome(chrome_driver_binary, chrome_options = options)
        driver.implicitly_wait(10)
        driver.get(url)
        elem = driver.find_element_by_id('history-observation-table')
        tBody = elem.find_element_by_tag_name('tbody')
        trList = tBody.find_elements_by_tag_name('tr')
        fieldsList = tuple()
        for tr in trList:
            allValues = tr.find_elements_by_tag_name('span')
            time = allValues[0].text.encode('ascii', 'ignore')
            time = convert24(time)
            time = re.sub('[^(0-9)]', '', time)
            time = int(time)
            if time/100 == planeTime/100:
                fieldsList = (float(allValues[2].text.encode('ascii', 'ignore')), float(allValues[8].text.encode('ascii', 'ignore')), \
                    str(allValues[10].text.encode('ascii', 'ignore')), float(allValues[12].text.encode('ascii', 'ignore')), float(allValues[21].text.encode('ascii', 'ignore')))
                break
    except: 
        driver.close()
    driver.close()
    return fieldsList

#make the table
def makeTable():
    #get filenames from user
    originalFilename = raw_input("What .csv file would you like to open? ")
    print originalFilename
    outputFilename = raw_input("What .csv file would you like to write to? (to create new, provide new filename with .csv ending) ")
    print outputFilename

    #read csv using pandas
    df1 = pd.read_csv(originalFilename)
    print df1 

    #go through dataframe
    for index, row in df1.iterrows():
        delayTime = row['ARRIVAL_DELAY']
        originAirport = row['ORIGIN_AIRPORT']

        #save every 25 entries
        if index % 25 == 0:
            df1.to_csv(outputFilename, encoding='utf-8', index = False)
        destinationAirport = row['DESTINATION_AIRPORT']
        year = row['YEAR']
        month = row['MONTH']
        day = row['DAY']
        departTime = int(row['SCHEDULED_DEPARTURE'])
        arrivalTime = int(row['SCHEDULED_ARRIVAL'])
        print "index: ",index
        print "orginial Airport: ", originAirport
        print "destination Airport: ", destinationAirport
        # get weather for departing and arrival
        try:
            departureWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format("K"+originAirport, year, month, day), departTime)
        except:
            try: 
                departureWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format("P"+originAirport, year, month, day), departTime)
            except: 
                try:
                    departureWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(originAirport, year, month, day), departTime)
                except: pass
        try: 
            arrivalWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format("K"+destinationAirport, year, month, day), arrivalTime)
        except:
            try:
                arrivalWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format("P"+destinationAirport, year, month, day), arrivalTime)
            except:
                try: 
                    arrivalWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(destinationAirport, year, month, day), arrivalTime)
                except: pass
        
        #write to the dataframe with the results
        if departureWeather != ():
            df1.loc[index, 'DEPART_TEMP'] = departureWeather[0]
            df1.loc[index, 'DEPART_HUMIDITY'] = departureWeather[1]
            df1.loc[index, 'DEPART_WINDIR'] = departureWeather[2]
            df1.loc[index, 'DEPART_WIND'] = departureWeather[3]
            df1.loc[index, 'DEPART_PRECIP'] = departureWeather[4]
        if arrivalWeather != ():
            df1.loc[index, 'ARRIVAL_TEMP'] = arrivalWeather[0]
            df1.loc[index, 'ARRIVAL_HUMIDITY'] = arrivalWeather[1]
            df1.loc[index, 'ARRIVAL_WINDIR'] = arrivalWeather[2]
            df1.loc[index, 'ARRIVAL_WIND'] = arrivalWeather[3]
            df1.loc[index, 'ARRIVAL_PRECIP'] = arrivalWeather[4]
        
    #perform final save
    df1.to_csv(outputFilename, encoding='utf-8', index = False)

makeTable()