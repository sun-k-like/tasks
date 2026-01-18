# backend/app/schemas/welfare.py
from pydantic import BaseModel
from typing import Optional, Dict

class WelfareInfo(BaseModel):
    title: str
    target: str
    benefit: str
    deadline: Optional[str] = "상시모집"

class ExtractionResult(BaseModel):
    is_welfare: bool
    raw_text: str
    extracted_info: Optional[WelfareInfo] = None