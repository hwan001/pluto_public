import random
from datetime import datetime, timedelta
from urllib.parse import uses_netloc

import json
from flask import Flask
#from flask_restx import Api, Resource
from flask import request, render_template, make_response, jsonify, session, redirect, url_for, escape
from flask_cors import CORS # 외부 접속 가능하게 해줌

import yfinance as yf

import web.config as config
import web.controller.function as controller
from plutodb import PlutoDB


app = Flask(__name__)
database = PlutoDB(config.db_server, config.db_id, config.db_pw)
app.secret_key = config.secret_key
app.config['SESSION_LIMIT_EXCEPTION'] = True
app.config['SESSION_COOKIE_LIMIT'] = 1


# 여러 함수를 import 하는 용도의 빈 클래스? 
# git  허브 코드 참고하여 작성 중 (용도 모름)
class Services:
    pass

def create_app(test_config = None):
    print("url : ", config.url)
    
    app.debug = False

    # app 객체의 외부 접속이 가능해짐 ? 
    #CORS(app)
    
    # Set config
    #if test_config is None:
    #    app.config.from_pyfile('config.py')
    #else:
    #    app.config.update(test_config)

    #SetUp Persistence Layer - Model
    #database = model.mongodb.connect_conn()
    #database = PlutoDB(config.db_id, config.db_pw)

    #SetUp Business Layer - Controller
    #services = Services

    #SetUp Presentation Layer - View
    
    return app


@app.route('/')
def main():    
    if 'id' not in session:
        return '<script>window.location.href="/signin";</script>'

    return render_template('main.html')

@app.route('/mypage', methods=['GET'])
#@login_required
def index():
    if 'id' not in session:
        return '<script>alert("로그인이 필요합니다."); window.location.href="/signin";</script>'

    tickers = ["TSLA", "META", "GOOGL"]
    list_data = {}
    for ticker in tickers:
        list_data[ticker] = [random.randrange(-10, 11) for i in range(12)]
    return render_template('mypage.html', tickers_len=len(tickers), tickers=tickers, list_data=list_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['id']
        user_password = request.form['pw']
        user_tickers = []
        
        if database.registerUser(user_name, controller.password_hash(user_password)):
            print(user_name, ': 계정 생성 완료')
        else:
            return '<script>alert("가입 실패 : 이미 존재하는 사용자입니다."); window.location.href="/signin";</script>'
        
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']
        
        if database.validateUser(username, controller.password_hash(password)):
            print(username, '님이(가) 로그인 했습니다.') # 이런 부분들은 나중에 로그용 함수로 변경
            tickers = ["qqq", "SPYD"] # 해당 부분은 유저 정보에 같이 포함시키면 좋을 듯

            session['id'] = username

            return render_template('mypage.html', url=config.url, tickers_len=len(tickers), tickers=tickers)
        else:
            print(username, '계정 로그인 시도 발생')
            return '<script>alert("로그인 실패 - 아이디와 비밀번호를 확인해주세요."); window.location.href="/signin"; </script>'
    
    return render_template('signin.html')


@app.route('/signout')
def signout():
    if 'id' not in session:
        return '<script>alert("로그인이 필요합니다."); window.location.href="/signin";</script>'
    
    print(session['id'], "님이 로그아웃 하셨습니다.")
    session.pop('id', None)
    
    return render_template('main.html')
        

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if 'id' not in session:
        return render_template('signin.html')

    if request.method == 'POST':
        try:
            ticker = request.form.get("ticker")
            startdate = request.form.get("startdate")
            #enddate = request.form.get("enddate")
            enddate = datetime.now()
            interval = request.form.get("interval")
            kind = request.form.get("kind")
            
            yf_Ticker = yf.Ticker(ticker)
            
            ticker_data = yf_Ticker.history(start=startdate, end=enddate, interval=interval)[kind]
            ticker_index = (lambda origin: [str(tmp.strftime("%Y-%m-%d")) for tmp in list(origin.index)])(ticker_data)
            ticker_value = (lambda origin: [round(tmp, 2) for tmp in list(origin.values)])(ticker_data)
            aver_step = (max(ticker_value) - min(ticker_value)) / len(ticker_value)
            
            ticker_index_str = json.dumps(ticker_index)
            ticker_value_str = json.dumps(ticker_value)
        except Exception as e:
            return render_template('error_500.html', ticker=ticker, exception_msg=e)   
        
    elif request.method == 'GET':
        ticker = ""
        ticker_index = []
        ticker_value = []
        aver_step = 0
        
        ticker_index_str = json.dumps(ticker_index)
        ticker_value_str = json.dumps(ticker_value)
        
    return render_template('graph.html', ticker=ticker, ticker_index=ticker_index_str, ticker_value=ticker_value_str, aver_step=aver_step)



# js
@app.route("/function.js", methods=["GET"])
def js_file():
    return make_response(render_template("/function.js"))

@app.route("/my_style.css", methods=["GET"])
def css_file():
    return make_response(render_template("/my_style.css"))


# error handling
@app.errorhandler(500)
def error_handling_500(error):
    #ticker = str(request.query_string, 'utf-8').replace("ticker=", "")
    ticker = "ticker"
    return render_template('error_500.html', ticker=ticker)
    #return jsonify({"Error Code : 500"})

@app.errorhandler(400)
def error_handling_400(error):
    #return render_template('error_400.html')
    return jsonify({"Error Code : 400"})