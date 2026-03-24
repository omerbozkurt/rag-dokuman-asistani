from langchain_ollama import OllamaLLM
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from rag_backend.config import Config

class OllamaBridge:
    def __init__(self):
        self.llm = OllamaLLM(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0.3
        )

    def create_rag_chain(self, retriever):
        """Ollama tabanlı yerel RAG zinciri oluşturur."""
        system_prompt = (
            "Sen uzman bir dökümantasyon asistanısın. Tamamen yerel bir model (Ollama) üzerinde çalışıyorsun. "
            "Sana verilen döküman parçalarını (context) kullanarak soruları yanıtla. "
            "Eğer cevabı dökümanlarda bulamazsan, 'Bilgi bulunamadı' de. "
            "Cevapların kısa, öz ve Türkçe olsun.\n\n"
            "BAĞLAM:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
        
        return rag_chain

    def get_answer(self, rag_chain, question: str):
        """Soruyu yanıtlar ve kaynakları döndürür."""
        response = rag_chain.invoke({"input": question})
        
        sources = set()
        for doc in response["context"]:
            sources.add(doc.metadata.get("source", "Bilinmeyen Kaynak"))
            
        return response["answer"], list(sources)
