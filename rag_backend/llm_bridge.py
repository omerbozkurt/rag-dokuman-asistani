from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from rag_backend.config import Config

class LLMBridge:
    def __init__(self):
        self.llm = ChatOpenAI(model=Config.LLM_MODEL, temperature=0.2)

    def create_rag_chain(self, retriever):
        """RAG zinciri oluşturur."""
        system_prompt = (
            "Sen uzman bir dökümantasyon asistanısın. "
            "Sana verilen bağlamı (context) kullanarak soruları yanıtla. "
            "Eğer cevabı bağlamda bulamazsan, bilmediğini söyle. "
            "Cevapları Türkçe ve profesyonel bir dilde ver.\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain

    def get_answer(self, rag_chain, question):
        """Soruyu yanıtlar."""
        response = rag_chain.invoke({"input": question})
        return response["answer"]
