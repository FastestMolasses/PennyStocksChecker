import requests

from bs4 import BeautifulSoup


def getPennyStocks():
    tickers = []
    html = requests.get('https://toppennystocks.org/stocks-under-5.php').text
    soup = BeautifulSoup(html, 'html.parser')
    # Two tables in the html that provide the penny stocks
    table1, table2 = soup.findAll('table', {'class': 'styled', 'valign': 'top'})

    # We iterate over odd entries because the even ones are empty
    # for some reason
    # Start at 3 because the first row is the header row
    for i in range(3, len(table1.contents), 2):
        # The first column of each row is the ticker
        tickers.append(table1.contents[i].contents[1].text)

    for i in range(3, len(table2.contents), 2):
        # The first column of each row is the ticker
        tickers.append(table2.contents[i].contents[1].text)

    return tickers


if __name__ == '__main__':
    tickers = getPennyStocks()
    print(tickers)
