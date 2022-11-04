import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

link = "https://www.tradingview.com/markets/bonds/prices-major/"
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://www.tradingview.com/markets/bonds/prices-major/', adapter)
session.mount('https://www.tradingview.com/markets/bonds/prices-major/', adapter)
response = session.get(link)
rawHtml = response.content
soupObtained = BeautifulSoup(rawHtml, features='html.parser')
s1 = soupObtained.find_all('table', class_="tv-data-table")
s2 = soupObtained.find_all('a', class_="tv-screener__symbol")
s3 = soupObtained.find_all('td', class_="v-data-table__row")

def scrap():
    data_list = []
    for tr in s1:
        # Find all data for each column
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        data_list.append(row)
    return data_list

def clean():
    data_list = scrap()
    for i in data_list:
        data_list = filter(lambda item: item not in ['\n', '\t'], i)
    '''
    for j in my_list:
        with open("data3" + ".csv", "a", encoding="utf-8", errors='ignore') as txtFile:
            for i in s2:
                txtFile.writelines(i)
    '''
    return data_list
for i in clean():
    print(i)