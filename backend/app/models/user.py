from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index= True)
    username= Column(String, unique=True, nullable=False)
    email= Column(String, unique=True, nullable=False, index = True)
    hashed_password = Column(String, nullable=False)

files = relationship("FileAnalysis", back_populates="user")
