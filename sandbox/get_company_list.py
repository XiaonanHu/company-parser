import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import string


def get_nasdaq(categ):
    """
    This script quickly download the company names and return their tickers in a DataFrame
    :return:
    """
    if categ == "nasdaq":
        # Get company list
        os.system("curl --ftp-ssl anonymous:jupi@jupi.com "
                  "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt "
                  "> nasdaq.lst")
        # clean the data
        os.system("tail -n +9 nasdaq.lst | cat | sed '$d' | sed 's/|/ /g' > "
                  "nasdaq.lst2")
        os.system("awk '{print $1}' nasdaq.lst2 > nasdaq.csv")
        data = pd.read_csv("data/nasdaq.csv", index_col=None, header=None, skiprows=35)  # The first 35 rows are junk
        data.columns=["Ticker"]
        print(data)


def get_nyse():
    company_name = []
    company_ticker = []
    for char in string.ascii_uppercase:
        letter = char.upper()
        URL = 'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=' + letter
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        odd_rows = soup.find_all('tr', attrs={'class': 'ts0'})
        even_rows = soup.find_all('tr', attrs={'class': 'ts1'})
        for i in odd_rows:
            row = i.find_all('td')
            company_name.append(row[0].text.strip())
            company_ticker.append(row[1].text.strip())
        for i in even_rows:
            row = i.find_all('td')
            company_name.append(row[0].text.strip())
            company_ticker.append(row[1].text.strip())

    comp_info = pd.DataFrame({'company_name': company_name, 'company_ticker': company_ticker})
    # #Data Cleaning
    comp_info = comp_info[comp_info['company_name'] != '']
    return comp_info


if __name__ == "__main__":
    c_info = get_nyse()
    print(c_info.shape)

