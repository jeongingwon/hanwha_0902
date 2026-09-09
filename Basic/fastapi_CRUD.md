# 🚀 FastAPI & CRUD 핵심 개념 완벽 가이드

## 1. CRUD란 무엇인가요?

**CRUD**는 거의 모든 웹 애플리케이션과 데이터베이스가 수행하는 **4가지 핵심 기본 동작**의 약자입니다.

* **C (Create):** 새로운 데이터를 **생성** (예: 회원가입, 글쓰기)
* **R (Read):** 데이터를 **조회** 및 열람 (예: 게시글 목록 읽기, 내 프로필 보기)
* **U (Update):** 기존 데이터를 **수정** (예: 회원정보 변경, 비밀번호 수정)
* **D (Delete):** 데이터를 **삭제** (예: 회원 탈퇴, 게시글 삭제)

---

## 2. CRUD와 HTTP 요청 메서드 매핑

클라이언트(웹/앱)는 서버에 요청을 보낼 때 **"어떤 목적의 작업인가"**를 알리기 위해 HTTP 메서드를 함께 전달합니다.

| CRUD 기능 | HTTP 메서드 | FastAPI 데코레이터 | 쉽게 이해하는 비유 |
| :--- | :--- | :--- | :--- |
| **Create (생성)** | `POST` | `@app.post()` | **양식 제출:** 작성한 정보(JSON)를 서버로 전송해 신규 등록 |
| **Read (조회)** | `GET` | `@app.get()` | **열람 요청:** 서버 데이터를 변경하지 않고 단순 조회 |
| **Update (수정)** | `PUT` / `PATCH` | `@app.put()` | **내용 교체:** 기존 데이터를 새로운 데이터로 덮어씀 |
| **Delete (삭제)** | `DELETE` | `@app.delete()` | **휴지통 비우기:** 특정 ID의 데이터를 서버에서 제거 |

---

## 3. CRUD 단계별 동작 원리

### ① Create (`POST`)
1. **데이터 전송:** 클라이언트가 저장할 데이터를 JSON 형태로 Body에 담아 요청
2. **타입 검증:** Pydantic이 데이터 형식과 필드 유효성 자동 검사
3. **저장 및 응답:** 데이터베이스에 등록 후 성공 메시지(`201 Created` 또는 `200 OK`) 반환

### ② Read (`GET`)
1. **조건 전달:** URL 경로(Path Parameter)나 쿼리(Query)로 조회 대상 지정
2. **데이터 검색:** DB에서 조건에 맞는 항목 검색
3. **결과 반환:** 데이터 반환 (대상이 없으면 `404 Not Found` 에러 전달)

### ③ Update (`PUT` / `PATCH`)
1. **대상 및 데이터 전달:** 수정할 대상 ID와 새로운 데이터를 함께 전달
2. **수정 방식 구분:**
   * **PUT:** 데이터 **전체**를 새로운 내용으로 교체
   * **PATCH:** 변경할 **일부 항목**만 선택적으로 수정
3. **갱신 반환:** DB 데이터 업데이트 후 변경된 정보 응답

### ④ Delete (`DELETE`)
1. **식별자 전달:** 삭제할 대상의 ID를 URL로 전달 (예: `/users/1`)
2. **제거 및 응답:** DB에서 해당 데이터 삭제 처리 후 결과 메시지 반환

---

## 4. FastAPI 핵심 보조 개념

### ① Pydantic (`BaseModel`)
* **역할:** 서버로 입력되는 데이터의 **타입과 규격을 자동으로 검증**하는 도구
* **예시:** `price: float`로 선언 시 문자열이 입력되면 FastAPI가 자동으로 차단
* **`model_dump()`:** Pydantic 객체를 파이썬 딕셔너리(`dict`)로 변환하는 메서드

### ② HTTPException (에러 처리)
* 처리 중 오류 발생 시 클라이언트에게 **표준 에러 코드**와 메시지를 전달
* **`400 Bad Request`:** 클라이언트의 요청 데이터가 잘못됨 (예: ID 중복)
* **`404 Not Found`:** 요청한 데이터나 경로를 찾을 수 없음

### ③ Swagger UI (자동 문서화)
* 서버 실행 후 `http://127.0.0.1:8000/docs` 접속 시 웹 화면에서 API를 바로 테스트 가능

---

## 5. 최소화 요약 코드 (참고용)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


db = {}


@app.get("/items/{item_id}")  # [R] READ
async def read_item(item_id: int):
    return db.get(item_id)


@app.post("/items/{item_id}")  # [C] CREATE
async def create_item(item_id: int, item: Item):
    db[item_id] = item.model_dump()
    return {"message": "생성 완료"}


@app.put("/items/{item_id}")  # [U] UPDATE
async def update_item(item_id: int, item: Item):
    db[item_id] = item.model_dump()
    return {"message": "수정 완료"}


@app.delete("/items/{item_id}")  # [D] DELETE
async def delete_item(item_id: int):
    db.pop(item_id, None)
    return {"message": "삭제 완료"}