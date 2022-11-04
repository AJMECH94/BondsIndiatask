import requests
import pdb
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, render_template
app = Flask(__name__)

link = "https://www.tradingview.com/markets/indices/quotes-major/"
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://www.tradingview.com/markets/indices/quotes-major/', adapter)
session.mount('https://www.tradingview.com/markets/indices/quotes-major/', adapter)
response = session.get(link)
rawHtml = response.content
soupObtained = BeautifulSoup(rawHtml, features='html.parser')
s1 = soupObtained.find('table', class_='table-DR3mi0GH')


def scrap():
    data_list = []
    for tr in s1.find_all('tr'):
        # Find all data for each column
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        data_list.append(row)
    return data_list


def data_frame():
    data_list = scrap()
    df1 = pd.DataFrame(data_list, columns=['Ticker', 'Price', 'Chg % 1D', 'Chg 1D', 'High 1D', 'Low 1D', 'Technical rating 1D'])
    df1 = df1.drop(df1.index[0])
    mask1 = df1['Ticker'] == "SPXS&P 500 Index"
    mask2 = df1['Ticker'] == "DJIDow Jones Industrial Average Index"
    mask3 = df1['Ticker'] == "SENSEXS&P BSE Sensex Index"
    mask4 = df1['Ticker'] == "NI225Nikkei 225 Index"
    df1 = df1[mask1 | mask2 | mask3 | mask4]
    return df1


@app.route('/tradequote', methods=("POST", "GET"))
def html_table():
    df1 = data_frame()
    return render_template('tradequote.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)


if __name__ == "__main__":
    app.run(debug=True, port=8000)