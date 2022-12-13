import pymongo
from pymongo import MongoClient

class PlutoMongoConnector:
    """
        DB 단위 연결을 만들어 컬렉션과 데이터를 제어함.
        DB 정보는 Config.py에 입력
    """
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)

    def get_all_db(self) -> list:
        """
        현재 연결된 Client에 존재하는 db 목록을 가져옴

        Returns:
            list[str]
        """
        return self.client.list_database_names()
        
    def check_db(self, db) -> bool:
        """
        전체 db 명 중에 해당 db가 있으면 True, 없을 경우 False

        Args:
            db 이름

        Returns:
            전체 db 명 중에 해당 db가 있으면 True, 없을 경우 False
        """
        if db in self.get_all_db():
            return True
        return False

    def get_db(self, db_name:str) -> pymongo.database.Database:
        """
        DB 반환, 다른 디비를 사용하고 싶을 경우 해당 메소드를 다시 호출하면 동일 서버의 다른 DB를 얻어올 수 있음.

        Args:
            db 이름

        Returns:
            db.get_database(db_name)
        """
        return self.client.get_database(db_name)

    def get_Collection(self, db_name, col_name):
        """
        입력받은 db_name의 col_name을 가져온다.
        해당 db에 col_name이 없을 경우, 생성

        Args:
            db 이름

        Returns:
            db.get_collection(col_name)
        """
        try:
            col = db_name.create_collection(col_name)
        except:
            col = db_name.get_collection(col_name)


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
    def is_empty(self, col, query):
        if len(list(col.find(query))) == 0:
            return True
        else:
            return False

    # 아이디가 디비에 존재하는지 검사함
    def dbcheck(self, col, user_name):
        return self.is_empty(col, {"user_name":user_name})

    # id와 해시된 패스워드를 디비에서 조회함, 해당 데이터가 존재할 경우 로그인 성공(True 반환)
    def dblogin(self, col, user_name, user_pw):
        return self.is_empty(col, {"user_name":user_name, "user_pw":user_pw})

    # 입력 받은 id에 해당하는 티커를
    def get_tickers(self, col, user_name):
        return col.find({"user_name":user_name}).limit(1)

    # 유저 삭제
    def remove_user(self, col, user_name):
        col.delete_one({"user_name":user_name})


if __name__ == "__main__":
    pmc = PlutoMongoConnector("192.168.55.231", 27017)
    print(pmc.get_all_db())

    print(pmc.get_Collection(pmc.get_db("test_db"), "test_collection"))
