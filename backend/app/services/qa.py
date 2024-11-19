import os
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


class QAService:
    @staticmethod
    def answer_question(vector_store_path: str, question: str):
        """
        Answer a question based on a loaded vector store
        """
        try:
            # Load vector store
            os.environ["OPENAI_API_KEY"] = "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"
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.load_local(vector_store_path, embeddings)
            
            # Create QA chain
            chain = load_qa_chain(OpenAI(), chain_type="stuff")
            
            # Get relevant documents
            docs = vector_store.similarity_search(question)
            
            # Get answer
            answer = chain.run(input_documents=docs, question=question)
            
            return answer
        
        except Exception as e:
            raise ValueError(f"Error processing question: {str(e)}")