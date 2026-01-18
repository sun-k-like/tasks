# backend/tests/unit/test_validator.py
import pytest
from app.agents.validator import WelfareValidator

@pytest.fixture
def validator():
    return WelfareValidator()

# ... 기존 테스트 유지 ...

def test_validate_voucher_keyword(validator):
    """새로 추가된 '바우처' 키워드 검증"""
    text = "에너지 바우처 신청 안내입니다."
    assert validator.validate(text) is True

def test_validate_application_keyword(validator):
    """새로 추가된 '신청' 키워드 검증"""
    text = "보육료 지원 신청 기간 공고"
    assert validator.validate(text) is True