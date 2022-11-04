import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, render_template

app = Flask(__name__)
link = "https://www.ccilindia.com/Pages/default.aspx"
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://www.ccilindia.com/Pages/default.aspx', adapter)
session.mount('https://www.ccilindia.com/Pages/default.aspx', adapter)
session.get(link)
response = requests.get(link)
rawHtml = response.content
soupObtained = BeautifulSoup(rawHtml, features='html.parser')
specificSoup = soupObtained.find('table', id='ctl00_m_g_f59666ea_ac72_4c24_8dcc_df32847c6421_ctl00_AjaxTabContainer_tpIndianMoneyMarket_gvIndianMoney')


def scrap():
    data_list = []
    i = 0
    for tr in specificSoup.find_all('tr'):
        # Find all data for each column
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        data_list.append(row)
        i = i+1
        if i==4:
            break
    return data_list


def data_frame():
    data_list = scrap()
    df1 = pd.DataFrame(data_list, columns=['Market', 'open', 'High', 'low', 'LTR', 'volumes', 'WAR', 'prev day WAR', 'prev day vol'])
    df1 = df1.drop(df1.index[0])
    return df1


@app.route('/ccilindia', methods=("POST", "GET"))
def html_table():
    df1 = data_frame()
    return render_template('simple.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
