class WelfareTextFactory:
    """다양한 복지 공고문 템플릿을 생성하는 데이터 공장"""

    @staticmethod
    def create_success_case(case_type="general"):
        """성공 케이스: 키워드가 포함된 실제 공고문 스타일"""
        templates = {
            "general": "2026년 하반기 청년 월세 지원 사업 공고. 대상자는 지금 신청하세요.",
            "voucher": "에너지 바우처 지급 안내. 전기요금 및 가스비 보조금을 지원합니다.",
            "subsidy": "육아 휴직 급여 및 아동 수당 신청 방법 안내 (행정 복지 센터)",
            "application": "희망 저축 계좌 신청 기간 안내. 자산 형성 지원금을 드립니다."
        }
        return templates.get(case_type, templates["general"])

    @staticmethod
    def create_fail_case(case_type="spam"):
        """실패 케이스: 키워드가 없거나 관련 없는 텍스트 (낙관적 편향 제거)"""
        templates = {
            "spam": "[광고] 지금 바로 클릭하고 100% 당첨 행운을 잡으세요!",
            "news": "내일은 전국적으로 비가 내릴 예정이며 기온이 낮아지겠습니다.",
            "empty": "",
            "short": "안녕하세요 반갑습니다."
        }
        return templates.get(case_type, templates["spam"])

    @staticmethod
    def create_edge_case():
        """예외 케이스: 특수문자나 아주 긴 텍스트"""
        return "!!!지원!!! @@@복지@@@ ###신청###" * 10
    

from tests.factories import WelfareTextFactory

def test_validate_with_factory(validator):
    # Given: 공장에서 '바우처' 성공 케이스 텍스트를 가져옴
    text = WelfareTextFactory.create_success_case("voucher")
    
    # When: 검증기를 실행함
    result = validator.validate(text)
    
    # Then: 결과는 True여야 함
    assert result is True