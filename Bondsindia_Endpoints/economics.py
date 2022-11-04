import requests
import pdb
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, render_template
app = Flask(__name__)
link = "https://economictimes.indiatimes.com/markets/forex/currency-converter"
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://economictimes.indiatimes.com/markets/forex/currency-converter', adapter)
session.mount('https://economictimes.indiatimes.com/markets/forex/currency-converter', adapter)
response = session.get(link)
rawHtml = response.content
soupObtained = BeautifulSoup(rawHtml, features='html.parser')
specificSoup = soupObtained.find('table', class_='tblData5')


def scrap():
    data_list = []
    for tr in specificSoup.find_all('tr'):
        # Find all data for each column
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        data_list.append(row)
    return data_list


def data_frame():
    data_list = scrap()
    df1 = pd.DataFrame(data_list, columns=['Currency', 'Price', 'Change', '%change'])
    df1 = df1.drop(df1.index[0])
    return df1


@app.route('/economics', methods=("POST", "GET"))
def html_table():
    df1 = data_frame()
    return render_template('economics.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)


if __name__ == "__main__":
    app.run(debug=True, port=8000)