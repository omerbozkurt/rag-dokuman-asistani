from langchain_google_genai import ChatGoogleGenerativeAI
try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    # Python 3.14 ve bazı özel ortamlarda langchain_classic gerekebiliyor
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate
from rag_backend.config import Config

class GeminiBridge:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.3
        )

    def create_rag_chain(self, retriever):
        """Gemini tabanlı RAG zinciri oluşturur."""
        system_prompt = (
            "Sen uzman bir dökümantasyon asistanısın. "
            "Sana verilen döküman parçalarını (context) kullanarak soruları yanıtla. "
            "Eğer cevabı dökümanlarda bulamazsan, 'Maalesef bu konuda dökümantasyonda bilgi bulamadım' de. "
            "Cevapların profesyonel, anlaşılır ve Türkçe olsun.\n\n"
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
        
        # Kaynakları topla (Unique set)
        sources = set()
        for doc in response["context"]:
            sources.add(doc.metadata.get("source", "Bilinmeyen Kaynak"))
            
        return response["answer"], list(sources)
