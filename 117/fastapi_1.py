import os
import base64
import requests
import xml.etree.ElementTree as ET

from fastapi import UploadFile, File
from fastapi import FastAPI, Form  # FastAPI와 Form 임포트 확인
from openai import OpenAI
from dotenv import load_dotenv

from pydantic import BaseModel # 상단 import에 추가 확인

# --- 데이터 모델 (Pydantic) ---

class OCRResponse(BaseModel):
    file_id: str
    raw_text: str

# 이후에 나올 에러를 대비해 세션과 요약 모델도 미리 정의하면 좋습니다.
class SessionResponse(BaseModel):
    session_id: str

class SummaryResponse(BaseModel):
    summary_data: dict

# --- FastAPI 앱 정의 ---
app = FastAPI(title="행정 용어 변환 및 검증 서비스 API")

# .env 파일에서 API_KEY 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# F-04-1: 이미지에서 텍스트 추출 (LLM Vision 활용) 
@app.post("/api/ocr", response_model=OCRResponse)
async def perform_llm_ocr(file_id: str = Form(...),image: UploadFile = File(...)):

    # 1. 파일 내용을 읽고 Base64로 인코딩
    contents = await image.read()
    base64_image = base64.b64encode(contents).decode('utf-8')

    # 2. OpenAI Vision API 호출
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Vision 기능을 지원하는 최신 모델
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "이 이미지(청년수당 포스터)에서 '지원대상', '연령요건', '소득요건' 등 핵심 내용을 요약해서 텍스트로 알려줘."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        }
                    ],
                }
            ],
            max_tokens=1000,
        )
        extracted_text = response.choices[0].message.content
    except Exception as e:
        return {"file_id": file_id, "raw_text": f"에러 발생: {str(e)}"}
    
    return {"file_id": file_id, "raw_text": extracted_text}

# 우리말샘 사전 검색 함수
def search_woorimal(word: str):
    api_key = os.getenv("WOORIMAL_API_KEY")
    url = f"https://opendict.korean.go.kr/api/search?key={api_key}&q={word}&target=1&part=word"
    
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        # 첫 번째 검색 결과의 정의(definition) 추출
        definition = root.find(".//definition").text
        return definition
    except:
        return "뜻풀이를 찾을 수 없습니다."
    
# F-06: 행정어 정보 강화 엔드포인트 예시
@app.post("/api/agent/enhance")
async def enhance_text(raw_text: str):
    # 테스트용 행정어 리스트 (실제로는 LLM이 단어를 골라내도록 고도화 가능)
    target_words = ["중위소득", "부양의무자"]
    enhanced_data = {}
    
    for word in target_words:
        if word in raw_text:
            enhanced_data[word] = search_woorimal(word)
            
    return {"original_text": raw_text, "definitions": enhanced_data}

# 통합 엔드포인트: OCR + 행정어 사전 검색
@app.post("/api/v1/extract-and-enhance")
async def extract_and_enhance(image: UploadFile = File(...)):
    # [Step 1] 이미지에서 텍스트 추출 (OpenAI Vision)
    contents = await image.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 공고문에서 '지원대상', '조건' 등 핵심 정보를 추출하고, 본문에 포함된 어려운 행정 용어들을 단어 리스트로 따로 뽑아줘."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ],
            }
        ],
    )
    raw_text = response.choices[0].message.content

    # [Step 2] 추출된 텍스트 내 주요 단어 사전 검색 (F-06)
    # 실제로는 LLM이 뽑아준 리스트를 사용하거나 아래처럼 주요 키워드를 매칭합니다.
    keywords = ["중위소득", "부양의무자", "건강보험료", "미취업"]
    definitions = {}
    for word in keywords:
        if word in raw_text:
            definitions[word] = search_woorimal(word)
            
    return {
        "raw_text": raw_text,
        "enhanced_info": definitions
    }