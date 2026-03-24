import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
import os

class DocLoader:
    def __init__(self, urls):
        self.urls = urls

    def load_web_docs(self):
        """Web sayfalarından dökümanları yükler."""
        loader = WebBaseLoader(self.urls)
        docs = loader.load()
        return docs

    def load_local_pdfs(self, folder_path):
        """Yerel PDF dosyalarını yükler."""
        from langchain_community.document_loaders import PyPDFLoader
        all_docs = []
        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                path = os.path.join(folder_path, file)
                loader = PyPDFLoader(path)
                all_docs.extend(loader.load())
        return all_docs
