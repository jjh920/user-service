import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api.database as sess


from api.routes import member

app = FastAPI()

# CORS 설정
origins = [
    ""  # 허용할 프론트엔드 도메인

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(member.router)


if __name__ == '__main__':
    sess.create_tables()
    uvicorn.run('main:app',host='0.0.0.0', port=8000, reload=True)

