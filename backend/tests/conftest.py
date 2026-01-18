import pytest
from unittest.mock import MagicMock
from app.agents.validator import WelfareValidator
from tests.factories import WelfareTextFactory

@pytest.fixture
def validator():
    return WelfareValidator()

@pytest.fixture
def factory():
    return WelfareTextFactory()

@pytest.fixture
def mock_openai_response():
    """GPT-4o Vision의 응답을 흉내 내는 가짜 데이터 (비용 0원)"""
    return {
        "choices": [{"message": {"content": "테스트용 복지 공고문입니다."}}]
    }

@pytest.fixture
def mock_extractor(mocker, mock_openai_response):
    """실제 API를 호출하지 않는 가짜 추출기"""
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    return mock_client