import pandas as pd
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

# from geekstogeeks.org
def convert24(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
    elif str1[-2:] == "AM":
        return str1[:-2]
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]

def getFields(url, planeTime):
    options = webdriver.ChromeOptions()
    options.binary_location = '/Users/vikas/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
    chrome_driver_binary = '/Users/vikas/Downloads/chromedriver'
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
        # print time
        if time/100 == planeTime/100:
            # for value in allValues:
            #     print value.text
            fieldsList = (float(allValues[2].text.encode('ascii', 'ignore')), float(allValues[8].text.encode('ascii', 'ignore')), \
            float(allValues[12].text.encode('ascii', 'ignore')), float(allValues[21].text.encode('ascii', 'ignore')))
            break
    driver.close()
    return fieldsList

df1 = pd.read_csv("flights.csv")
late = 0
nLate = 0
for index, row in df1.iterrows():
    delayTime = row['ARRIVAL_DELAY']
    originAirport = row['ORIGIN_AIRPORT']
    destinationAirport = row['DESTINATION_AIRPORT']
    year = row['YEAR']
    month = row['MONTH']
    day = row['DAY']
    departTime = int(row['SCHEDULED_DEPARTURE'])
    arrivalTime = int(row['SCHEDULED_ARRIVAL'])
    departureWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(originAirport, year, month, day), departTime)
    arrivalWeather = getFields('https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(destinationAirport, year, month, day), arrivalTime)
    df1.loc[index, 'DEPART_TEMP'] = departureWeather[0]
    df1.loc[index, 'DEPART_HUMIDITY'] = departureWeather[1]
    df1.loc[index, 'DEPART_WIND'] = departureWeather[2]
    df1.loc[index, 'DEPART_PRECIP'] = departureWeather[3]
    df1.loc[index, 'ARRIVAL_TEMP'] = arrivalWeather[0]
    df1.loc[index, 'ARRIVAL_HUMIDITY'] = arrivalWeather[1]
    df1.loc[index, 'ARRIVAL_WIND'] = arrivalWeather[2]
    df1.loc[index, 'ARRIVAL_PRECIP'] = arrivalWeather[3]
    print(departureWeather)
    if math.isnan(delayTime) or delayTime >=15 :
        df1.loc[index,'ARRIVAL_DELAY'] = 1
        late += 1
    else:
        df1.loc[index,'ARRIVAL_DELAY'] = 0
        nLate += 1
    if index == 5:
        break
print ("late", late, "nLate: ", nLate)

df1.to_csv("flights1.csv", encoding='utf-8', index = False)
