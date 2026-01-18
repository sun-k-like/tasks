🚀 LLM Agent 기반 행정어 순화 서비스 (PoC)
  이 프로젝트는 복잡한 인프라 대신 **비동기 처리(Async)**와 메모리 기반(In-Memory) 설계를 활용하여, 대량의 행정 문서 이미지를 효율적으로 분석하고 순화하는 LLM 에이전트 시스템입니다.

🛠️ 주요 설계 원칙 (Operational Strategy)
  In-Memory 데이터 처리: 초기 단계의 민첩성을 위해 별도의 DB 없이 서버 메모리 내에서 즉시 데이터를 처리합니다.

  FastAPI 비동기 최적화: async/await 구조를 통해 여러 사용자의 동시 요청을 병렬로 수용하여 응답 지연을 최소화했습니다.

  에이전트 모듈화: main.py(지휘소)와 agents.py(실무진)를 분리하여 향후 기능 확장이 용이하도록 설계했습니다.

📊 성능 검증 결과 (Postman Load Test)
  Postman Runner를 통한 부하 테스트 결과, 초기 모델의 안정성을 입증했습니다.

  성공률: 100% (20/20회 성공)

  평균 응답 시간: 4.02초 (이미지 분석~최종 검증 포함)

🔒 보안 정책
  .gitignore 적용: API Key(.env), 가상환경(venv/), 임시 파일 등을 격리하여 보안 유출을 원천 차단했습니다.

🏃 시작하기

  # 1. 라이브러리 설치
  pip install -r requirements.txt
  
  # 2. 서버 실행
  uvicorn main:app --reload
