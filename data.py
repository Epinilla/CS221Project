import pandas as pd
import math
from bs4 import BeautifulSoup
import requests
import html5lib
from selenium import webdriver
import time

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

    query = 'https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(originAirport, year, month, day)
    request = requests.get(query)

    # browser = webdriver.Chrome("/Users/Jleis/Downloads/chromedriver_win32/chromedriver.exe")
    # browser.get(query)
    # html = browser.page_source
    # newSoup = BeautifulSoup(html, features = 'html.parser')
    # mydivs = newSoup.findAll("div", {"class": "region-content-observation"})
    # # print ("request: ", query)
    # print ("divs: ", mydivs)
    # break

    for i in range(100):
        # soup = BeautifulSoup(request.text)
        soup = BeautifulSoup(request.text, features = 'html.parser')
        # print ("request: ", query)
        mydivs = soup.findAll("div", {"class": "region-content-observation"})
        print ("divs: ", mydivs)
        # body = soup.find(text="World population").find_previous('p')
        # if str(body.text).find('loading...') > 1:
            # print (body.text)
            # break
        time.sleep(5)
        request = requests.get(query)
        # html = requests.get("http://www.theworldcounts.com/counters/shocking_environmental_facts_and_statistics/world_population_clock_live").text

    break



    soup = BeautifulSoup(request.text, features = 'html.parser')
    print ("request: ", query)
    mydivs = soup.findAll("div", {"class": "region-content-observation"})
    print ("divs: ", mydivs)

    if math.isnan(delayTime) or delayTime >=15 :
        df1.loc[index,'ARRIVAL_DELAY'] = 1
        late += 1
    else:
        df1.loc[index,'ARRIVAL_DELAY'] = 0
        nLate += 1
    if index == 0:
        break
print ("late", late, "nLate: ", nLate)
# df1.to_csv("flights1.csv", encoding='utf-8', index = False)
