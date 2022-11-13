from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

import sys
import subprocess
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cvxpy'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cvxopt'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyPortfolioOpt'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pulp'])

def f1():
    plt.style.use('fivethirtyeight')

    assets = ["GOOGL", "MO", "NET", "CSCO"]

    weights = np.array([0.2] * len(assets))

    stockStartDate = '2010-01-01'
    today = datetime.today().strftime("%Y-%m-%d")
    df = pd.DataFrame()

    for stock in assets:
        df[stock] = web.DataReader(stock, data_source='yahoo', start=stockStartDate, end=today)['Close']

    title = "portfolio close price history"
    my_stocks = df
    plt.figure(figsize=(12.2, 4.5))

    for c in my_stocks.columns.values:
        plt.plot(my_stocks[c], label=c)
    plt.title(title)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price USD ($)', fontsize=18)
    plt.legend(my_stocks.columns.values, loc='upper left')
    #plt.show()

    returns = df.pct_change()
    cov_matrix_annual = returns.cov() * 252
    port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
    port_volatility = np.sqrt(port_variance)

    portfolioSimpleAnnualReturn = np.sum(returns.mean()*weights) * 252

    percent_var = str(round(port_variance) * 100) + '%'
    percent_vols = str(round(port_volatility) * 100) + '%'
    percent_ret = str(round(portfolioSimpleAnnualReturn, 2) * 100) + '%'

    print("Expected annual return : " + percent_ret)
    print("Annual volatility/standard deviation/risk : " + percent_vols)
    print("Annual variance : " + percent_var)

    from pypfopt.efficient_frontier import EfficientFrontier
    from pypfopt import risk_models
    from pypfopt import expected_returns

    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    print (cleaned_weights)
    ef.portfolio_performance(verbose=True)


    from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
    latest_prices = get_latest_prices(df)
    weights = cleaned_weights

    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=15000)
    allocation, leftover = da.lp_portfolio()

    print("Discret allocation: ", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))


import random 
sys.setrecursionlimit(2500)
global sum
global list_주식수

def f2(보유주식수, 평균단가):
    global sum
    global list_주식수
    
    if 보유주식수 <= 0:
        return
    
    현재가격 = random.randrange(int(평균단가 - 30), int(평균단가 + 30))
    
    # 상폐
    if 현재가격 <= 0:
        list_주식수.append("상폐")
        return
    
    원래가치 = 보유주식수 * 평균단가
    현재가치 = 보유주식수 * 현재가격
    손익 = 현재가치 - 원래가치
    손실율 = 손익 / 원래가치
    print("현재 가격 : ", 현재가격, "보유 주식 수 : ", 보유주식수, ", 가치 : ", 원래가치)
    추매주식수 = int(보유주식수 * 손실율 * -1)
    추매주식가치 = 추매주식수 * 현재가격
    
    if 추매주식수 < 0:
        print(-1 * 추매주식수, "주 매도, 매도 금액 : $", 추매주식가치, "\n")
    else:
        print(추매주식수, "주 매수, 매수 금액 : $", 추매주식가치, "\n")
    
    if 보유주식수 + 추매주식수 <= 0:
        list_주식수.append([0, 평균단가, 현재가격])
        return
    
    보유주식수 += 추매주식수
    list_주식수.append([보유주식수, 평균단가, 현재가격])
    
    원래가치 += 추매주식가치
    sum += 추매주식가치
    
    평균단가 = 원래가치 / 보유주식수
    
    # 계산된 가격을 현재값으로 다시 계산 (0주가 될때깢)
    f2(보유주식수, 평균단가)
        

def f3(보유주식수, 평균단가, 현재주가):
    현재가치 = 보유주식수 * 평균단가
    실제가치 = 보유주식수 * 현재주가
    손익 = 실제가치 - 현재가치
    손실율 = 손익 / 현재가치
    #print("현재 가격 : ", 현재주가, ", 보유 주식 수 : ", 보유주식수, ", 내 평단 : ", 평균단가, ", 현재 가치 : ", 현재가치)
    
    추매주식수 = -1 * (int(보유주식수 * 손실율)) # -일 경우 매도
    추매주식가격 = round(추매주식수 * 현재주가, 2) # 현재 주가 만큼 추가 매수, 거기에 필요한 금액
    #print("추매할 주식 수 : ", 추매주식수, ", 추매주식의 가격 : ", 추매주식가격)
    
    if 보유주식수 + 추매주식수 <= 0:
        예상주식수 = 0
        예상가치 = 현재가치
        예상평단 = 0
    else: 
        예상주식수 = 보유주식수 + 추매주식수
        예상가치 = 현재가치 + 추매주식가격
        예상평단 = 예상가치 / 예상주식수
    
    return 예상주식수, round(예상가치, 2), round(예상평단, 2), 추매주식가격, 추매주식수
    
if __name__ == "__main__":
    #sum = 0
    #list_주식수 = []

    #f2(102, 124.76) # 현재보유한주식수, 현재기준1주당가격

    #print(list_주식수)
    #print(-1 * sum, "달러 이득, ", 1420 * sum * -1, ", 거래 횟수 : ", len(list_주식수), "회, 걸린 기간 : ", len(list_주식수)//12, "년 ", len(list_주식수)%12, " 개월")
    
    
    list_tmp = [102] # 보유한주식수
    list_tmp2 = [124.76] # 평단
    list_cur = [83] #현재가격
    거래횟수 = 100
    변동폭 = 20
    sum = 0
    
    for i in range(거래횟수):
        tmp = f3(list_tmp[i], list_tmp2[i], list_cur[i])
        if tmp[0] <= 0:
            sum += list_tmp[i] * list_cur[i]
            print(" [전체 매도] 현재 보유 주식 : ", list_tmp[i], ", 수익 : $", list_tmp[i] * list_cur[i])
            break
        
        list_tmp.append(tmp[0])
        list_tmp2.append(tmp[2]) 

        cur = random.randrange(int(list_cur[i] - 변동폭), int(list_cur[i] + 변동폭))
        while(cur <= 0):
            cur = random.randrange(int(list_cur[i] - 변동폭), int(list_cur[i] + 변동폭))
                                   
        list_cur.append(cur)
        
        매수매도 = "매도" if tmp[3] < 0 else "매수"

        print(f"{i+1}회 현재 주가 : ${list_cur[i]}, 보유 개수 : {list_tmp[i]}주(${round(list_tmp[i] * list_tmp2[i], 2)}), {abs(tmp[4])}주(${abs(tmp[3])}) 추가 " + 매수매도 + f" -> 현재 보유 {tmp[0]}주(${tmp[2]}, ${tmp[1]})")
        
        if 매수매도 == "매도": sum += abs(tmp[3])
        else: sum -= abs(tmp[3])

        print(" > 현재 거래 수익 : ", -1 * tmp[3], ", 누적 거래 수익 : $", sum, "\n")
    print("총 수익 : $", sum)