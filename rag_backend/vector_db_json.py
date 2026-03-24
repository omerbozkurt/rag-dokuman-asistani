import json
import os
from typing import List
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from rag_backend.config import Config

class JSONVectorDB:
    def __init__(self):
        # Google'ın döküman vektörleştirme modeli
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="embedding-001",
            google_api_key=Config.GOOGLE_API_KEY
        )

    def load_from_json(self, json_file: str):
        """JSON dosyasını okur ve FAISS vektör veritabanına yükler."""
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON dosyası bulunamadı: {json_file}")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []
        for item in data:
            doc = Document(
                page_content=item["text"],
                metadata=item["metadata"]
            )
            documents.append(doc)

        # FAISS veritabanını oluştur
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        return vectorstore
