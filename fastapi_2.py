from fastapi import FastAPI, UploadFile, File, HTTPException
import asyncio

app = FastAPI()

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

# 2. 메인 분석 API (단일 응답 구조)
@app.post("/v1/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # [Step 1] 이미지 수신 (In-Memory 저장)
        image_content = await file.read()
        
        # [Step 2] 비동기 체이닝 (LLM 에이전트 흐름)
        # 각 단계는 await를 통해 Non-blocking으로 처리되어 여러 요청을 동시에 수용함
        
        # Vision 에이전트 처리
        extracted_text = await vision_agent(image_content)
        
        # RAG 검색 진행
        rag_context = await rag_agent(extracted_text)
        
        # 순화어 변환 진행
        refined_result = await refine_agent(extracted_text, rag_context)
        
        # Fact Check 및 Omission Check (순화 이후 진행)
        verification = await fact_check_agent(refined_result)
        
        # [Step 3] 최종 결과 단일 응답 반환
        return {
            "status": "success",
            "result": {
                "original_text": extracted_text,
                "refined_text": refined_result,
                "verification": verification
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))