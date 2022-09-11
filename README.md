# Pluto - Stock Recommander
주식 종목을 추천해주는 AI 서비스

# 소스 구성
> ## financedb_updater.py
>    스케줄러에 등록해두어 주기적인 DB 업데이트를 수행한다
>    MongoDB 를 사용하며 Ticker 목록을 불러와
>    해당되는 모든 차트를 업데이트 한다.
>    장중인 데이터는 업데이트 하지 않는다.

> ## eval.py
>    

> ## train.py
>    TensorFlow 기반으로 제작된 학습 소스이다.
>    90일 데이터로, 앞으로의 30일의 등락폭을 예측 할 수 있도록
>    데이터를 학습한다.

> ## run.py
>    Pluto의 Web서버를 실행시킨다.

> ## web
>    AI를 통해 학습된 데이터를 사용자에게 UI로 보여줄 Flask 기반의 웹 서버이다.

> ## Dockerfile, Docker 관련 스크립트 파일
>    컨테이너 빌드를 위한 파일
