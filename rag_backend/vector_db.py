from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from rag_backend.config import Config
import os

class VectorDBManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.db = None

    def initialize_db(self, documents=None):
        """Vector DB oluşturur veya var olanı yükler."""
        if documents:
            self.db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=Config.CHROMA_PATH
            )
        else:
            self.db = Chroma(
                persist_directory=Config.CHROMA_PATH,
                embedding_function=self.embeddings
            )
        return self.db

    def get_retriever(self, search_kwargs={"k": 5}):
        """Arama için retriever döndürür."""
        if not self.db:
            self.initialize_db()
        return self.db.as_retriever(search_kwargs=search_kwargs)
