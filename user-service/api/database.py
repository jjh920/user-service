import sqlalchemy
from sqlalchemy.orm import sessionmaker
from api.models.member import Base

# db_url = 'mysql+pymysql://username:password@hostname:3306/dbname'
db_url = 'mysql+pymysql://test:test@10.100.10.228:3306/test'



engine = sqlalchemy.create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(engine)


# 데이터베이스 세션 의존성 생성
def get_db():
    with SessionLocal() as db:
        yield db
