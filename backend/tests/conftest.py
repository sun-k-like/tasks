import pytest
from app.agents.validator import WelfareValidator
from tests.factories import WelfareTextFactory

@pytest.fixture
def validator():
    """기존 test_validator.py의 validator()와 이름이 같아도 개별 파일 내 우선순위가 적용되므로 안전합니다."""
    return WelfareValidator()

@pytest.fixture
def factory():
    """새로운 테스트 파일들에서 사용할 데이터 공장 배달 서비스"""
    return WelfareTextFactory()