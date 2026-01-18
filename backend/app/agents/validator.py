# backend/app/agents/validator.py

class WelfareValidator:
    def __init__(self):
        # 기획서 2.1.2의 '키워드 분석'을 위한 기초 사전 [cite: 33]
        self.welfare_keywords = ["복지", "공고", "지원", "보조금", "수당", "급여", "청년", "행정"]

    def validate(self, text: str) -> bool:
        """
        추출된 텍스트를 기준으로 서비스 제공 가능 여부를 판단 (기획서 2.1.2) [cite: 32, 33]
        """
        if not text:
            return False
        
        # 단순 키워드 매칭 로직 (추후 LLM으로 고도화 가능)
        return any(keyword in text for keyword in self.welfare_keywords)