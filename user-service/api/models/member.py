from datetime import datetime

from sqlalchemy import Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Member(Base):
    __tablename__ = 'member'

    mno = Column(Integer, primary_key=True, autoincrement=True, index=True)     # 회원번호
    userid = Column(String(18), nullable=False, unique=True)                    # 아이디
    passwd = Column(String(255), nullable=False)                                 # 패스워드
    name = Column(String(20), nullable=False)                                   # 이름
    phone = Column(String(11), nullable=False, unique=True)                     # 전화번호
    email = Column(String(50), nullable=False, unique=True)                     # 이메일
    regdate = Column(String(20))                                                # 생성일자







