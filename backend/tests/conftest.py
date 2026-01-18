# backend/tests/conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_openai_response():
    """GPT-4o Vision의 응답을 흉내 내는 가짜 데이터입니다."""
    return {
        "choices": [
            {
                "message": {
                    "content": "이것은 테스트용 복지 공고문 텍스트입니다. 지원 대상: 청년, 혜택: 수당 지급."
                }
            }
        ]
    }

@pytest.fixture
def mock_extractor(mocker, mock_openai_response):
    """실제 API를 호출하지 않는 가짜 추출기(Extractor)를 만듭니다."""
    # app.agents.extractor 내부의 OpenAI 호출부를 가로챕니다.
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    return mock_client