import os

from dotenv import load_dotenv
from openai import OpenAI


def main():
    # .env 파일의 환경변수 불러오기
    load_dotenv()

    # API Key 가져오기
    api_key = os.getenv("OPENAI_API_KEY")

    # API Key 존재 여부 확인
    if not api_key:
        print("❌ OPENAI_API_KEY가 설정되어 있지 않습니다.")
        return

    print("🔑 API Key가 설정되어 있습니다.")

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=api_key)

    # API 호출
    try:
        response = client.responses.create(
            model="gpt-5",
            input="안녕하세요. API 연결 테스트입니다."
        )

        print("✅ API 연결 성공!")
        print("🤖 응답:")
        print(response.output_text)

    except Exception as e:
        print("❌ API 호출 실패")
        print(f"오류: {e}")


if __name__ == "__main__":
    main()
