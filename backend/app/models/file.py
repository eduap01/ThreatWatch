from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class FileAnalysis(Base):
    __tablename__ = "file_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    sha256 = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)
    result_summary = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    analyzed_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="files")

