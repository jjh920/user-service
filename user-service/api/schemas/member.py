from pydantic import BaseModel
from datetime import datetime


class MemberBase(BaseModel):
    userid: str
    name: str
    email: str
    phone: str


class MemberLogin(BaseModel):
    userid: str
    passwd: str


class MemberCreate(MemberBase):
    passwd: str


class Member(MemberBase):
    mno: int
    # regdate: datetime
    regdate: str

    class Config:
        from_attributes=True


class Token(BaseModel):
    access_token: str
    token_type: str