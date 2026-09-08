# FastAPI 기본 개념 및 활용 요약 가이드

FastAPI의 기본 개념, 특징, 설치 방법, 서버 실행 및 결과 확인 방법까지 정리한 가이드 문서입니다.

---

## 1. FastAPI 개요

**FastAPI**는 파이썬 3.8 이상에서 고성능 API 서버를 구축하기 위해 사용하는 현대적이고 빠른 웹 프레임워크입니다.

### 주요 특징
* **높은 성능 (High Performance):** `Starlette`과 `Pydantic`을 기반으로 제작되어 Node.js, Go 언어 수준의 매우 빠른 성능을 자랑합니다.
* **비동기 처리 (Async/Await):** 파이썬의 `async` / `await` 구문을 완벽하게 지원하여 높은 동시 요청을 효율적으로 처리합니다.
* **자동 API 문서화:** 서버를 실행하면 Swagger UI(`/docs`)와 ReDoc(`/redoc`) 대화형 문서가 자동으로 생성됩니다.
* **타입 힌트 및 자동 검증:** 파이썬 표준 타입 힌트를 활용해 코드 완성도를 높이고, 올바르지 않은 데이터 요청 시 자동으로 에러 응답을 반환합니다.

---

## 2. 파이썬 웹 프레임워크 비교

| 구분 | FastAPI | Flask | Django |
| :--- | :--- | :--- | :--- |
| **주 목적** | 고성능 REST API / 마이크로서비스 | 마이크로 웹 앱 | 대규모 풀스택 웹 애플리케이션 |
| **속도/성능** | 매우 빠름 (비동기 기본 지원) | 보통 (동기 위주) | 보통 (동기 위주) |
| **자동 문서화** | 기본 제공 (Swagger UI / ReDoc) | 별도 패키지 필요 | 별도 패키지 필요 |
| **학습 난이도** | 낮음 ~ 보통 | 매우 낮음 | 높은 편 |

---

## 3. 설치 방법 (pip)

터미널 또는 명령 프롬프트(cmd)에서 아래 명령어를 실행합니다.

```bash
# 기본 FastAPI 및 실행 서버(Uvicorn) 함께 설치 (권장)
pip install fastapi "uvicorn[standard]"

# FastAPI 패키지만 단독 설치한 경우 (추후 uvicorn 추가 설치 필요)
pip install fastapi
pip install uvicorn
```

---

## 4. 서버 실행 방법

터미널에서 작성한 파이썬 파일(예: `main.py`)을 실행합니다.

* **방법 1: FastAPI CLI 사용 (개발 모드)**
  ```bash
  fastapi dev main.py
  ```

* **방법 2: Uvicorn 직접 실행 (권장)**
  ```bash
  uvicorn main:app --reload
  ```
  * `main`: 실행할 파이썬 파일명 (`main.py`)
  * `app`: `main.py` 내의 `FastAPI()` 객체 변수명
  * `--reload`: 코드 수정 시 서버 자동 재시작

---

## 5. 결과 확인 방법 및 주소

서버 실행 후 웹 브라우저 주소창에 아래 URL을 입력하여 결과를 확인합니다.

* **기본 API 응답 확인:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
  * 작성한 엔드포인트의 JSON 데이터 응답을 확인합니다.
* **Swagger UI 대화형 API 문서:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  * API 목록을 시각적으로 확인하고 직접 웹상에서 테스트(Try it out)할 수 있습니다.
* **ReDoc 대안 API 문서:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
  * 읽기 전용 형태의 깔끔하게 정돈된 API 명세서를 제공합니다.