# backend/app/agents/validator.py

class WelfareValidator:
    def __init__(self):
        # 기획서 2.1.2 '키워드 분석'을 위한 기초 사전
        # 리소스 최적화: 이 키워드가 없으면 이후 고비용 LLM 로직을 실행하지 않음
        self.welfare_keywords = [
            "복지", "공고", "지원", "보조금", "수당", 
            "급여", "청년", "행정", "바우처", "신청"
        ]

    def validate(self, text: str) -> bool:
        """
        추출된 텍스트를 기준으로 서비스 제공 가능 여부를 판단 (기획서 2.1.2)
        """
        if not text:
            return False
        
        # 텍스트에 복지 관련 핵심 키워드가 하나라도 포함되어 있는지 확인
        # (낙관적 편향 제거: 관련 없는 텍스트는 여기서 즉시 차단)
        return any(keyword in text for keyword in self.welfare_keywords)