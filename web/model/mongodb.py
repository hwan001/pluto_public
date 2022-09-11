from pymongo import MongoClient

# 서버와의 연결을 만들어서 반환해줌
def connect_server(host, port):
    return MongoClient(host, port)

# 디비와의 연결을 만들어서 반환해줌
def connect_db(host, port, db_name):
    return MongoClient(host, port).get_database(db_name)

# 컬렉션과의 연결을 만들어서 반환해줌
def connect_collection(host, port, db_name, collection_name):
    return MongoClient(host, port).get_database(db_name).get_collection(collection_name)


# 입력받은 서버의 디비와 컬렉션에 유저 데이터를 추가할 수 있음
def signup_server(server_name, db_name, collection_name, user_info):
    db = server_name.get_database(db_name)
    
    try:
        col = db.create_collection(collection_name)
    except:
        col = db.get_collection(collection_name)

    col.insert_one(user_info)

# 입력받은 디비와 컬렉션에 유저 데이터를 추가할 수 있음
def signup_db(db_name, collection_name, user_info):
    try:
        col = db_name.create_collection(collection_name)
    except:
        col = db_name.get_collection(collection_name)

    col.insert_one(user_info)


# 입력받은 컬렉션에 유저 데이터를 추가할 수 있음
def signup_collection(collection_name, user_info):
    collection_name.insert_one(user_info)



# 불러온 쿼리의 반환 결과 개수가 0이면 해당 쿼리의 결과가 없다고 판단
def is_empty(col, query):
    if len(list(col.find(query))) == 0:
        return True
    else:
        return False
    
# 아이디가 디비에 존재하는지 검사함
def dbcheck(col, user_name):
    return is_empty(col, {"user_name":user_name})

# id와 해시된 패스워드를 디비에서 조회함, 해당 데이터가 존재할 경우 로그인 성공(True 반환)
def dblogin(col, user_name, user_pw):
    return is_empty(col, {"user_name":user_name, "user_pw":user_pw})

# 입력 받은 id에 해당하는 티커를
def get_tickers(col, user_name):
    return col.find({"user_name":user_name}).limit(1)

# 유저 삭제
def remove_user(col, user_name):
    col.delete_one({"user_name":user_name})

