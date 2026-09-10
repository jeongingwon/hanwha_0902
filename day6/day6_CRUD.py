from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    username: str
    email: EmailStr  # EmailStr을 import 해두셨으니 활용하시면 이메일 형식 검증도 자동으로 됩니다!
    password: str


# [수정 완료] 콜론(:) 문법으로 변경 및 필드명을 username, email로 일치시킴
class UserUpdate(BaseModel):
    username: str
    email: EmailStr


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "안녕하세요~"}


# http://127.0.0.1:8000 URL 경로에서 이름을 받아서 결과로 출력
@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"반갑습니다 {name}님!"}


# 클라이언트(웹/앱)가 '/users/signup' 주소로 데이터를 보낼 때(POST) 실행할 함수 연결
@app.post("/users/signup")
async def signup(user: UserSignup):
    # 입력된 데이터 검사 (비밀번호가 8글자보다 짧은지 확인)
    if len(user.password) < 8:
        # 검사 실패 시: "잘못된 요청(400)" 에러를 발생시키고 아래 코드는 실행하지 않음
        raise HTTPException(
            status_code=400,  # 400 = "입력값이 잘못되었습니다"라는 표준 인터넷 에러 코드
            detail="비밀번호는 최소 8자리 이상이어야 합니다.",  # 사용자에게 보여줄 에러 이유
        )

    # 검사 통과 시: 가입 성공 메시지와 회원 정보를 결과로 응답 (보안상 비밀번호는 제외)
    return {
        "status": 201,  # 201 = "새로운 데이터가 성공적으로 만들어졌습니다"라는 성공 코드
        "message": f"{user.username}님의 회원가입이 완료되었습니다.",
        "user_info": {
            "username": user.username,
            "email": user.email,
        },
    }


# 테스트용 임시 데이터베이스 (가상 데이터)
fake_users_db = {
    1: {"username": "coder123", "email": "coder@example.com"},
    2: {"username": "dev_kim", "email": "kim@example.com"},
}


# DELETE 요청: Path Parameter로 삭제할 유저의 ID를 전달받음
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # 삭제할 데이터가 DB에 존재하는지 확인
    if user_id not in fake_users_db:
        # 데이터가 없으면 404 (Not Found) 에러 반환
        raise HTTPException(
            status_code=404, detail=f"ID가 {user_id}인 사용자를 찾을 수 없습니다."
        )

    # 데이터 존재 시 삭제 처리
    deleted_user = fake_users_db.pop(user_id)

    # 삭제 완료 메시지 및 삭제된 정보 반환
    return {
        "status": "success",
        "message": f"ID {user_id} ({deleted_user['username']}) 계정이 성공적으로 삭제되었습니다.",
    }


# PUT /users/{user_id} 경로로 요청이 오면 기존 데이터를 수정하는 함수 실행
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    # 1. 수정할 유저가 존재하지 않는 경우 404 에러 발생
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=404, detail=f"ID가 {user_id}인 사용자를 찾을 수 없습니다."
        )

    # 2. 유저 정보 업데이트 (새로운 데이터로 덮어쓰기)
    fake_users_db[user_id] = {"username": user.username, "email": user.email}

    # 3. 수정 성공 메시지 및 변경된 유저 정보 반환
    return {
        "status": "success",
        "message": f"ID {user_id} 사용자 정보가 성공적으로 수정되었습니다.",
        "updated_user": fake_users_db[user_id],
    }