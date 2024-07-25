from datetime import timedelta, datetime
from typing import Optional
import bcrypt
import jwt
from sqlalchemy.orm import Session
from api.schemas import member as pym
from api.models import member as sqlm

# 비밀번호 해싱을 위한 솔트값
SALT = bcrypt.gensalt()

# 토큰 생성시 사용할 비밀키
SECRETKEY = 'Hello, World!!'

# 회원가입 처리
def register(db: Session, member: pym.MemberCreate):
    # 비밀번호를 바이트 문자열로 해싱
    hashed_passwd = bcrypt.hashpw(member.passwd.encode('utf-8'), SALT)
    print(hashed_passwd)

    # 데이터베이스 모델 객체 생성
    db_user = sqlm.Member(**member.model_dump())
    db_user.passwd = hashed_passwd  # 바이트 문자열 저장
    db_user.regdate = datetime.now().isoformat(' ', 'seconds')

    # 사용자 추가 및 커밋
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return pym.Member.from_orm(db_user)

# 액세스 토큰 생성
def generate_access_token(userid: str, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode = {'sub': userid, 'exp': expire}
    encode_jwt = jwt.encode(to_encode, SECRETKEY, algorithm='HS256')

    return encode_jwt

# 로그인 처리
def authenticate(db: Session, user: pym.MemberLogin) -> Optional[str]:
    db_user = db.query(sqlm.Member).filter(sqlm.Member.userid == user.userid).first()

    if not db_user:
        return None

    # 데이터베이스에서 가져온 해시된 비밀번호가 문자열인 경우 바이트 문자열로 변환
    if isinstance(db_user.passwd, str):
        db_user_passwd = db_user.passwd.encode('utf-8')
    else:
        db_user_passwd = db_user.passwd

    # 비밀번호 검증
    if not bcrypt.checkpw(user.passwd.encode('utf-8'), db_user_passwd):
        return None

    token = generate_access_token(user.userid)
    return token
