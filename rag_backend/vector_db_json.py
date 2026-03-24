import json
import os
from typing import List
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from rag_backend.config import Config

class JSONVectorDB:
    def __init__(self):
        # 404 hatalarına karşı en güncel ve stabil yapılandırma
        self.google_api_key = Config.GOOGLE_API_KEY
        try:
            # 1. Tercih: Yeni nesil Gemini Embedding Modeli (En stabil olan)
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                task_type="retrieval_document",
                google_api_key=self.google_api_key
            )
            self.embeddings.embed_query("test")
        except Exception:
            try:
                # 2. Tercih: Alternatif model (Task type ile)
                self.embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/text-embedding-004",
                    task_type="retrieval_document",
                    google_api_key=self.google_api_key
                )
            except Exception as e:
                raise Exception(f"Vektörleştirme modellerine erişilemedi: {str(e)}")

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
