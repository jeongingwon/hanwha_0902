# ⚡ Streamlit(front) x FastAPI(Back) 프로토콜 아키텍처

Streamlit(프론트엔드)과 FastAPI(백엔드)를 활용한 Agent 시스템의 **핵심 아키텍처** 및 **데이터 왕복 흐름** 정리 가이드입니다.

---

## 1. 한눈에 보는 3계층 아키텍처 다이어그램

```text
[ 사용자 (User) ]
       │
       │ 1. 입력 (질문/명령)
       ▼
 ┌───────────┐
 │ Streamlit │  <-- [ Presentation Tier ] UI 화면 / 사용자 입력 수집 & 시각화
 └───────────┘
       │ ▲
  HTTP │ │ HTTP
  Request│ │ Response (JSON)
       ▼ │
 ┌───────────┐
 │  FastAPI  │  <-- [ Application Tier ] 비즈니스 로직 / API 처리 & 데이터 검증
 └───────────┘
       │ ▲
       │ │ LLM 호출 & 도구/데이터 조회
       ▼ │
 ┌───────────┐
 │ DB / LLM  │  <-- [ Data / AI Tier ] OpenAI API / Agent / Vector DB
 └───────────┘