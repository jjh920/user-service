from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import jwt
from api.database import get_db
from api.services.member import register, authenticate
from api.schemas import member as pym
from api.models import member as sqlm

router = APIRouter()

# OAuth2PasswordBearer를 통해 토큰을 가져옵니다
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 비밀키를 환경 변수에서 가져오거나 설정합니다
SECRETKEY = 'Hello, World!!'  # 비밀키는 환경 변수로 설정하는 것이 좋습니다

@router.get("/")
async def index():
    return {"message": "Hello World"}

@router.get("/member", response_model=list[pym.Member])
async def list_users(db: Session = Depends(get_db)):
    members = db.query(sqlm.Member).all()
    return [pym.Member.from_orm(mb) for mb in members]

@router.post("/member", response_model=pym.Member)
async def create_user(member_create: pym.MemberCreate, db: Session = Depends(get_db)):
    return register(db, member_create)

@router.post("/login", response_model=pym.Token)
async def login_user(member_login: pym.MemberLogin, db: Session = Depends(get_db)):
    token = authenticate(db, member_login)

    if not token:
        raise HTTPException(status_code=401, detail='로그인 실패!! - 아이디 또는 비밀번호가 틀립니다!')

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=pym.Member)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return pym.Member.from_orm(user)

def get_current_user(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=["HS256"])
        userid = payload.get("sub")
        if userid is None:
            return None
        user = db.query(sqlm.Member).filter(sqlm.Member.userid == userid).first()
        return user
    except jwt.PyJWTError:
        return None
