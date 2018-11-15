# from bs4 import BeautifulSoup
# from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

options = webdriver.ChromeOptions()
options.binary_location = '/Users/vikas/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
chrome_driver_binary = '/Users/vikas/Downloads/chromedriver'
driver = webdriver.Chrome(chrome_driver_binary, chrome_options = options)
url = 'https://www.wunderground.com/history/daily/MSP/date/2015-1-1?fbclid=IwAR0s_TVUZxQOLnQOaDhV25MKQCS_TXiNZWOba_xewQs1VFNOKPhj1Hy7PI8'
driver.implicitly_wait(10)
driver.get(url)
elem = driver.find_element_by_id('history-observation-table')
tBody = elem.find_element_by_tag_name('tbody')
trList = tBody.find_elements_by_tag_name('tr')
fieldsList = tuple()
for tr in trList:
    allValues = tr.find_elements_by_tag_name('span')
    time = allValues[0].text.encode('ascii', 'ignore')
    pm = False
    if time[-2:] == 'PM':
        pm = True
    time = re.sub('[^(1-9)]', '', time)
    time = int(time)
    if pm:
        time += 1200
    # print time
    if time == 1836:
        # for value in allValues:
        #     print value.text
        fieldsList = (float(allValues[2].text.encode('ascii', 'ignore')), float(allValues[8].text.encode('ascii', 'ignore')), \
        float(allValues[12].text.encode('ascii', 'ignore')), float(allValues[21].text.encode('ascii', 'ignore')))
print fieldsList
driver.close()
