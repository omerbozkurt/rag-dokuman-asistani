import streamlit as st
import sys
import os

# Uygulama dosya sisteminde kk dizini bul ve PATH'e ekle
sys.path.append(os.getcwd())

from rag_backend.gemini_bridge import GeminiBridge
from frontend.components.chat_bubbles import chat_message_html, inject_styles
from data_ingestion.md_ingestor import MarkdownIngestor
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from rag_backend.vector_db_json import JSONVectorDB

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="RAG AI Asistanı",
    page_icon="🤖",
    layout="centered"
)

# ... (Sidebar ve CSS aynı kalıyor) ...
inject_styles()

with st.sidebar:
    st.markdown('<p class="sidebar-title">🤖 Bulut Tabanlı RAG</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="sidebar-text">
    Yeni dökümanlar yükleyerek asistanınızı geliştirebilirsiniz (Markdown veya PDF).
    </p>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Döküman Yükle (Markdown veya PDF)", 
        type=["md", "pdf"], 
        accept_multiple_files=True,
        key="doc_uploader"
    )

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Vektör DB ve Chain Yükleme (PDF desteği eklendi)
def setup_system(uploaded_files=None):
    try:
        gemini = GeminiBridge()
        vdb_manager = JSONVectorDB()
        ingestor = MarkdownIngestor()
        
        all_docs = []
        
        # 1. Eğer yüklenmiş dosya varsa onları işle
        if uploaded_files:
            for uploaded_file in uploaded_files:
                filename = uploaded_file.name
                if filename.endswith(".pdf"):
                    # PDF İşleme
                    file_chunks = ingestor.process_pdf(uploaded_file.read(), filename)
                else:
                    # Markdown İşleme
                    content = uploaded_file.read().decode("utf-8")
                    file_chunks = ingestor.process_text(content, filename)
                
                for chunk in file_chunks:
                    all_docs.append(Document(
                        page_content=chunk["text"],
                        metadata=chunk["metadata"]
                    ))

        
        # 2. Eğer yüklenmiş dosya yoksa ama yerel JSON varsa onu yükle
        elif os.path.exists("data/processed_docs.json"):
            st.session_state.vectorstore = vdb_manager.load_from_json("data/processed_docs.json")
        
        # 3. Eğer dökümanlar hazırsa Vektör DB'yi oluştur/güncelle
        if all_docs:
            st.session_state.vectorstore = FAISS.from_documents(all_docs, vdb_manager.embeddings)
        
        if st.session_state.vectorstore:
            st.session_state.rag_chain = gemini.create_rag_chain(
                st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
            )
            return True
        return False
    except Exception as e:
        st.error(f"Sistem başlatılamadı: {str(e)}")
        return False

# Dosya yüklendiğinde sistemi tetikle
if uploaded_files and (st.session_state.rag_chain is None or st.session_state.get('last_upload_count') != len(uploaded_files)):
    with st.spinner("📂 Dökümanlar işleniyor..."):
        if setup_system(uploaded_files):
            st.session_state.last_upload_count = len(uploaded_files)
            st.success("✅ Dökümanlar başarıyla yüklendi ve işlendi!")
        else:
            st.warning("⚠️ Dökümanlar işlenemedi.")


# Ana Ekran
st.markdown("""
<div style="text-align: center; padding: 4rem 0 2rem 0;">
    <h1 style="margin-bottom: 0;">Doküman Asistanı</h1>
    <p class="tagline">Yapay Zeka Destekli Akıllı Dökümantasyon Analizi</p>
</div>
""", unsafe_allow_html=True)


# Chat Geçmişini Göster
for message in st.session_state.messages:
    chat_message_html(
        message["role"], 
        message["content"], 
        message.get("sources")
    )

# Chat Input
if prompt := st.chat_input("Bir soru sorun..."):
    # Sistemi hazırla (Lazy load)
    if setup_system():
        # Kullanıcı mesajını göster
        st.session_state.messages.append({"role": "user", "content": prompt})
        chat_message_html("user", prompt)

        # Yanıt Üretme (Spinner ile)
        with st.spinner("🔍 Gemini dökümanları analiz ediyor..."):
            try:
                gemini = GeminiBridge()
                answer, sources = gemini.get_answer(st.session_state.rag_chain, prompt)
                
                # Mesajı kaydet ve göster
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "sources": sources
                })
                chat_message_html("assistant", answer, sources)
                st.rerun() # UI'ı güncellemek için
            except Exception as e:
                st.error(f"Yanıt üretilirken bir hata oluştu: {str(e)}")
    else:
        st.warning("Sistem hazır değil. Lütfen verilerin yüklü olduğundan emin olun.")
