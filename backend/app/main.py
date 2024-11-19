from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os

from sqlalchemy.orm import Session

from app.db.session import engine, Base, get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse, QuestionRequest, AnswerResponse
from app.services.document import DocumentService
from app.services.qa import QAService

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Document storage configuration
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# API endpoints
@app.post("/documents/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create database entry
        db_document = Document(
            filename=file.filename,
            file_path=file_path
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Process the PDF and create vector store
        text = DocumentService.process_pdf(file_path)
        vector_store = DocumentService.create_vector_store(text)
        
        # Save vector store
        vector_store.save_local(f"{UPLOAD_DIR}/vector_store_{db_document.id}")
        
        return db_document
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/question/", response_model=AnswerResponse)
async def ask_question(
    question_request: QuestionRequest,
    db: Session = Depends(get_db)
):
    # Get document from database
    document = db.query(Document).filter(Document.id == question_request.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Get answer
        answer = QAService.answer_question(
            f"{UPLOAD_DIR}/vector_store_{document.id}", 
            question_request.question
        )
        
        return AnswerResponse(
            answer=answer,
            document_id=question_request.document_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents