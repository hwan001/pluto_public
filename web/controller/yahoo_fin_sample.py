
import sys
import subprocess

try:
    from yahoo_fin.stock_info import *

except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    from yahoo_fin.stock_info import *


# https://algotrading101.com/learn/yahoo-finance-api-guide/ -> 가이드!
if __name__ == '__main__':
    ticker = "JEPI"

    if ticker in tickers_dow():
        print("dow")
    if ticker in tickers_other():
        print("other")
    if ticker in tickers_sp500():
        print("sp500")
    if ticker in tickers_ftse250():
        print("ftse250") 
    if ticker in tickers_ftse100():
        print("ftse100")
    if ticker in tickers_ibovespa():
        print("ibovespa")
    if ticker in tickers_nasdaq():
        print("nasdaq")

    print(get_data(ticker))


