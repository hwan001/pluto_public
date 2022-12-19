
global current_ticker_price_table
global userdata_table

# 현재 가격 테이블
current_ticker_price_table = {
    "MO":101,
    "GOOGL":83,
    "U":32.52
}

# 유저 데이터
userdata_table = {
    "hwan001":{
        "GOOGL":{
            "number_of_stock":102, 
            "average_price":124.76,
            "total_amount": 12725.52,
            "total_profit":0,
        }, 
        "MO":{
            "number_of_stock":100, 
            "average_price":45.23,
            "total_amount": 4523,
            "total_profit":0,
        }
    },
    "test":{
        "U":{
            "number_of_stock":25, 
            "average_price":52.62,
            "total_amount": 1315.5,
            "total_profit":0,
        }
    }
}


def TM_ALGO_2(보유주식수:int, 평균단가:float, 현재주가:float) -> list:
    현재가치 = 보유주식수 * 평균단가
    실제가치 = 보유주식수 * 현재주가
    손익 = 실제가치 - 현재가치
    손실률 = 손익 / 현재가치
    #print("현재 가격 : ", 현재주가, ", 보유 주식 수 : ", 보유주식수, ", 내 평단 : ", 평균단가, ", 현재 가치 : ", 현재가치)
    
    추매주식수 = -1 * (int(보유주식수 * 손실률)) # -일 경우 매도
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
    
    return 추매주식수, 손실률


# 트레이딩 모듈 사용해서 결과를 업데이트해줄 데코레이터
def TM_Decorator(username:str = "", ticker:str = "") -> dict:
    '''
    input : number_of_stock, average_price 
    output : {"total_profit":float, "number_of_stock":int, "expected_average_price":float}
    '''    
    global current_ticker_price_table
    global userdata_table
    
    if "" == ticker or "" == username:
        return "No Data"
    
    # username과 ticker로 필요한 데이터 얻어오기
    current_price = current_ticker_price_table[ticker]     
    number_of_stock = userdata_table[username][ticker]["number_of_stock"]
    average_price = userdata_table[username][ticker]["average_price"]
    total_sum = userdata_table[username][ticker]["total_amount"]
    
    # 알고리즘 계산 결과
    additional_stock, 손실률 = TM_ALGO_2(number_of_stock, average_price, current_price) 
    
    # 반영
    total_number_of_stock = number_of_stock + additional_stock
    total_number_of_stock = userdata_table[username][ticker]["number_of_stock"] = total_number_of_stock
    predict_average_price = userdata_table[username][ticker]["average_price"] = round(((number_of_stock * average_price) + (additional_stock * current_price)) / total_number_of_stock, 2)
    userdata_table[username][ticker]["total_amount"] += (additional_stock * current_price)
    
    if additional_stock < 0: # 매도 누적
        userdata_table[username][ticker]["total_profit"] += (additional_stock * current_price * -1)
    
    #print(f"현재 주가 : ${current_price}, 보유 개수 : {number_of_stock}주, 내 평단 : {average_price}, 추가 구매 : {additional_stock}")
    #print(f"-> 예상 주수 : {total_number_of_stock}주, 예상 평단 : ${predict_average_price}, 손실률 : {round(손실률*100, 2)}%")
    
    

username = "test"
userticker = "U"
values = [43.2, 36.3, 41.5, 45.6, 46.7, 49.3, 43.5, 50.1, 52.3, 56.5, 60]
exchange_rate = 1320

print("["+username + ", " + userticker + "]")
print(current_ticker_price_table[userticker], userdata_table[username][userticker], format(int(round(userdata_table[username][userticker]["total_amount"] * exchange_rate, 0)), ','), "원")
for i in range(len(values)):
    print("Trade " + str(i+1) + " : ", end='')
    current_ticker_price_table[userticker] = values[i]
    TM_Decorator(username, userticker)
    print(current_ticker_price_table[userticker], userdata_table[username][userticker], format(int(round(userdata_table[username][userticker]["total_amount"] * exchange_rate, 0)), ','), "원")
    