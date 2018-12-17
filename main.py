import string
import requests

from bs4 import BeautifulSoup


def getPennyStocks():
    tickers = []
    html = requests.get('https://toppennystocks.org/stocks-under-5.php').text
    soup = BeautifulSoup(html, 'html.parser')
    # Two tables in the html that provide the penny stocks
    table1, table2 = soup.findAll(
        'table', {'class': 'styled', 'valign': 'top'})

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


def getStocksFromURL():
    # Don't include the last 2 because the url is the same
    for letter in string.ascii_uppercase[:-2]:
        # Pick the correct site based on the letter
        url = 'http://www.allstocks.com/pennystocks/OTC_BB_Stocks/OTCBB_{0}_s/otcbb_{1}_s.html'.format(
            letter, letter.lower())
        if letter < 'M':
            pass
        elif letter < 'X':
            url = 'http://www.allstocks.com/pennystocks/OTC_BB_Stocks/OTCBB_{0}_s/OTCBB_{1}_s/otcbb_{2}_s.html'.format(
                chr(ord(letter) - 12), letter, letter.lower())
        else:
            url = 'http://www.allstocks.com/pennystocks/OTC_BB_Stocks/OTCBB_L_s/OTCBB_X_Y_Z_s/otcbb_x_y_z_s.html'

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        stocks = soup.findAll('td', {'width': '492'})[3]
        print(stocks)
        stocks = stocks.p
        print(stocks)
        return
        # stocks = [i.text for i in stocks.contents]
        # print(stocks)
        # return


def getEstimate(symbol):
    html = requests.get(
        f'https://www.marketwatch.com/investing/stock/{symbol}/analystestimates').text
    soup = BeautifulSoup(html, 'html.parser')
    # Find all the anaylst estimates
    numbers = soup.findAll('td', {'class': 'current'})
    if not numbers:
        return None
    return ','.join([i.text for i in numbers])


if __name__ == '__main__':
    tickers = getPennyStocks()
    print(f'Found {len(tickers)} penny stocks')

    # The first line of the csv file should be the column titles
    lines = ['SYMBOL,BUY,OVERWEIGHT,HOLD,UNDERWEIGHT,SELL,MEAN\n']
    for i in tickers:
        print(f'Analyzing {i}...')
        estimate = getEstimate(i)
        if not estimate:
            continue
        lines.append(i + ',' + estimate + '\n')

    with open('stocks.csv', 'w') as f:
        for i in lines:
            f.write(i)

    # print(getStocksFromURL())
