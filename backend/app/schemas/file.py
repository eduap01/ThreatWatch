from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, Any
import json

class FileAnalysisBase(BaseModel):
    filename: str
    content_type: str
    sha256: str
    result_summary: Optional[Any] = None  # aquí admitimos dict o str

    # si viene como string, lo convertimos a dict
    @field_validator("result_summary", mode="before")
    def parse_summary(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return v
        return v

class FileAnalysisCreate(FileAnalysisBase):
    pass

class FileAnalysisOut(FileAnalysisBase):
    id: int
    uploaded_at: datetime
    analyzed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
