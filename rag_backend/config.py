import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "data/vector_store")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo")
    EMBEDDING_MODEL = "text-embedding-3-small"
