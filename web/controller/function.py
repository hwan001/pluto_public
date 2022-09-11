import hashlib

# 해시쳐서 반환 -> 디비 관련 기능이 아님 (다른 곳으로 이동 필요)
def password_hash(pw):
    return hashlib.sha256(bytes('PLU/'+pw+'/TO', 'utf-8')).hexdigest()
