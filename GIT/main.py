from fastapi import FastAPI, UploadFile, File, HTTPException
import agents  # 위에서 만든 agents.py 파일을 가져옵니다.

app = FastAPI()

@app.post("/v1/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        image_content = await file.read()
        
        # agents.py에 있는 함수들을 순서대로 호출합니다.
        extracted_text = await agents.vision_agent(image_content)
        rag_context = await agents.rag_agent(extracted_text)
        refined_result = await agents.refine_agent(extracted_text, rag_context)
        verification = await agents.fact_check_agent(refined_result)
        
        return {
            "status": "success",
            "result": {
                "original": extracted_text,
                "refined": refined_result,
                "check": verification
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))