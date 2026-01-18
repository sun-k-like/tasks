# backend/tests/unit/test_validator.py
import pytest
from app.agents.validator import WelfareValidator

@pytest.fixture
def validator():
    return WelfareValidator()

def test_validate_welfare_text_success(validator):
    """복지 관련 키워드가 포함된 경우 성공해야 함"""
    text = "2026년 청년 수당 지원 공고문입니다."
    assert validator.validate(text) is True

def test_validate_unrelated_text_fail(validator):
    """복지와 무관한 텍스트는 거절되어야 함 (낙관적 편향 제거)"""
    text = "오늘 점심 메뉴는 돈가스입니다."
    assert validator.validate(text) is False

def test_validate_empty_text(validator):
    """빈 텍스트 입력 시 에러 없이 False 반환"""
    assert validator.validate("") is False