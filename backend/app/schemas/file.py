from datetime import datetime

from pydantic import BaseModel


class FileAnalysisBase(BaseModel):
    filename: str
    content_type: str
    sha256: str
    result_summary: str | None = None
class FileAnalysisCreate(FileAnalysisBase):
    pass

class FileAnalysisOut(FileAnalysisBase):
    id: int
    uploaded_at: datetime
    analyzed_at: datetime | None = None

    class Config:
        from_attributes = True