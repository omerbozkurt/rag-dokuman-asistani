import streamlit as st
import sys
import os

# Uygulama dosya sisteminde kök dizini bul ve PATH'e ekle
sys.path.append(os.getcwd())

from rag_backend.gemini_bridge import GeminiBridge
from frontend.components.chat_bubbles import chat_message_html, inject_styles
from data_ingestion.md_ingestor import MarkdownIngestor
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from rag_backend.vector_db_json import JSONVectorDB

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Doküman Asistanı",
    page_icon="🤖",
    layout="wide" # Geniş mod daha profesyonel durur
)

# Stil Enjeksiyonu
inject_styles()

# Sidebar Tasarımı
with st.sidebar:
    st.markdown('<p class="sidebar-title">🤖 DOKÜMAN ASİSTANI</p>', unsafe_allow_html=True)
    
    # Sistem Durumu Kartı
    st.markdown("""
    <div class="system-status-card">
        <div class="status-row">
            <span>Zeka Modeli</span>
            <span style="display: flex; align-items: center; gap: 5px;">
            Gemini Flash <div class="status-dot"></div>
            </span>
        </div>
        <div class="status-row">
            <span>Vektör DB</span>
            <span>FAISS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Bilgi Kaynaklarını Yükle", 
        type=["md", "pdf"], 
        accept_multiple_files=True,
        key="doc_uploader"
    )

    if st.button("Sohbeti Temizle", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.session_state.rag_chain = None
        st.session_state.last_upload_count = 0
        st.rerun()

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Vektör DB ve Chain Yükleme
@st.cache_resource
def get_system_components():
    """Gemini ve Vektör DB bileşenlerini bir kez oluşturur."""
    gemini = GeminiBridge()
    vdb_manager = JSONVectorDB()
    ingestor = MarkdownIngestor()
    return gemini, vdb_manager, ingestor

def setup_system(uploaded_files=None):
    try:
        gemini, vdb_manager, ingestor = get_system_components()
        all_docs = []
        
        # Eğer zaten bir vectorstore varsa ve yeni dosya yoksa işlem yapma
        if not uploaded_files and st.session_state.vectorstore:
            return True

        # 1. Eğer yüklenmiş dosya varsa onları işle
        if uploaded_files:
            total_chunks = 0
            for uploaded_file in uploaded_files:
                filename = uploaded_file.name
                if filename.endswith(".pdf"):
                    file_chunks = ingestor.process_pdf(uploaded_file.read(), filename)
                else:
                    content = uploaded_file.read().decode("utf-8")
                    file_chunks = ingestor.process_text(content, filename)
                
                total_chunks += len(file_chunks)
                for chunk in file_chunks:
                    all_docs.append(Document(
                        page_content=chunk["text"],
                        metadata=chunk["metadata"]
                    ))
            
            if total_chunks > 0:
                # Vektör DB'yi sıfırdan oluştur (Önceki verileri temizle)
                st.session_state.vectorstore = FAISS.from_documents(all_docs, vdb_manager.embeddings)
                st.toast(f"✅ {len(uploaded_files)} dosya işlendi, {total_chunks} bilgi parçası hazır!", icon="🧠")
            else:
                st.warning("⚠️ Dökümanlardan metin çıkarılamadı (PDF resim tabanlı olabilir).")
                return False
        
        # 2. Eğer yüklenmiş dosya yoksa ama yerel JSON varsa onu yükle (YEDEK OLARAK)
        elif os.path.exists("data/processed_docs.json") and not st.session_state.vectorstore:
            st.session_state.vectorstore = vdb_manager.load_from_json("data/processed_docs.json")
        
        if st.session_state.vectorstore:
            # Retriever'ı yenile
            st.session_state.rag_chain = gemini.create_rag_chain(
                st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
            )
            return True
        return False
    except Exception as e:
        st.error(f"❌ Sistem başlatılamadı: {str(e)}")
        # Hata durumunda state'i temizle ki sonsuz döngü olmasın
        st.session_state.vectorstore = None
        st.session_state.rag_chain = None
        return False

# Dosya yüklendiğinde sistemi tetikle
if uploaded_files and (st.session_state.rag_chain is None or st.session_state.get('last_upload_count') != len(uploaded_files)):
    with st.spinner("📂 Bilgi ağacı örülüyor..."):
        if setup_system(uploaded_files):
            st.session_state.last_upload_count = len(uploaded_files)
            st.toast("✅ Bilgi tabanı güncellendi!", icon="🚀")
        else:
            st.warning("⚠️ Dökümanlar işlenemedi.")

# Ana Ekran Layout
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>Doküman Asistanı</h1>
        <p class="tagline">Yapay Zeka Destekli Akıllı Analiz Sistemi</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat Alanı
    chat_placeholder = st.container()
    
    with chat_placeholder:
        for message in st.session_state.messages:
            chat_message_html(
                message["role"], 
                message["content"], 
                message.get("sources")
            )

    # Padding for chat input
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# Chat Input (Bottom Fixed)
if prompt := st.chat_input("Dökümanlarınız hakkında bir soru sorun..."):
    with col2:
        # Kullanıcı mesajını anında kaydet ve göster
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Sistemi hazırla (Lazy load)
        if setup_system() or uploaded_files:
            # Yanıt Üretme
            with st.spinner("🔍 Gemini dökümanları derinlemesine analiz ediyor..."):
                try:
                    gemini = GeminiBridge()
                    # RAG Chain kontrolü
                    if st.session_state.rag_chain is None:
                        setup_system(uploaded_files)
                    
                    if st.session_state.rag_chain:
                        answer, sources = gemini.get_answer(st.session_state.rag_chain, prompt)
                        
                        # Mesajı kaydet
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer, 
                            "sources": sources
                        })
                        st.rerun()
                    else:
                        st.error("❌ RAG sistemi başlatılamadı. Lütfen dökümanların yüklendiğinden emin olun.")
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        st.error("⚠️ **API Kotası Doldu:** Günlük limitinize ulaştınız. Lütfen bir süre sonra tekrar deneyin.")
                    else:
                        st.error(f"❌ Kritik Hata: {error_msg}")
        else:
            st.warning("⚠️ Lütfen önce bir döküman yükleyerek asistanı bilgilendirin.")
            st.rerun() # Kullanıcı mesajının görünmesi için
