import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

os.environ["OPENAI_API_KEY"] = "sk-xxx"

class DocumentService:
    @staticmethod
    def process_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def create_vector_store(text: str):
        """Create vector store from document text"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(text)
        
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts, embeddings)
        return vector_store