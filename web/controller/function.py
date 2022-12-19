import hashlib
import logging

# 해시쳐서 반환 -> 디비 관련 기능이 아님 (다른 곳으로 이동 필요)
def password_hash(pw):
    return hashlib.sha512(bytes('PLU/'+pw+'/TO', 'utf-8')).hexdigest()

class PlutoLogger:
    """
    pluto Logger
    - 데코레이터, 함수 호출 등으로 로깅용 컬렉션에 로그를 기록
    
    """
    def __init__(self):
        pass

