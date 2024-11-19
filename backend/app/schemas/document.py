from pydantic import BaseModel
from datetime import datetime
from typing import List

class DocumentBase(BaseModel):
    filename: str

class DocumentResponse(DocumentBase):
    id: int
    upload_date: datetime
    
    class Config:
        orm_mode = True

class QuestionRequest(BaseModel):
    document_id: int
    question: str

class AnswerResponse(BaseModel):
    answer: str
    document_id: int