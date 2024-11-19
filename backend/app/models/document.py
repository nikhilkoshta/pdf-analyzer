from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.now)
    file_path = Column(String)