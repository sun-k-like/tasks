import asyncio

# 1. 시뮬레이션: 각 LLM 에이전트 기능 (실제로는 LLM API 호출)
async def vision_agent(image_bytes: bytes):
    await asyncio.sleep(1)  # 비동기 I/O 시뮬레이션
    return "이미지에서 추출된 공공기관 안내문 텍스트"

async def rag_agent(text: str):
    await asyncio.sleep(1)
    return f"관련 정책 원문 데이터 (RAG 검색 결과: {text})"

async def refine_agent(extracted_text: str, rag_data: str):
    await asyncio.sleep(1)
    return "순화된 행정어 결과물"

async def fact_check_agent(refined_text: str):
    await asyncio.sleep(1)
    return "Fact Check 완료: 이상 없음"