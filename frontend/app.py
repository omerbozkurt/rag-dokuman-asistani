import streamlit as st
from rag_backend.vector_db_json import JSONVectorDB
from rag_backend.gemini_bridge import GeminiBridge
from frontend.components.chat_bubbles import chat_message_html, inject_styles

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
    Bu sistem <b>Google Gemini API</b> kullanır. Bilgisayarınıza dökümanlar dışında hiçbir şey yüklemeniz gerekmez.
    </p>
    """, unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# Vektör DB ve Chain Yükleme (Gemini versiyonu)
def setup_system():
    if st.session_state.rag_chain is None:
        try:
            vdb_manager = JSONVectorDB()
            vectorstore = vdb_manager.load_from_json("data/processed_docs.json")
            
            gemini = GeminiBridge()
            st.session_state.rag_chain = gemini.create_rag_chain(vectorstore.as_retriever(search_kwargs={"k": 3}))
            return True
        except Exception as e:
            st.error(f"Sistem başlatılamadı. Lütfen API anahtarınızı kontrol edin: {str(e)}")
            return False
    return True

# Ana Ekran
st.title("🚀 Doküman Asistanı")
st.markdown("Modern RAG Sistemi ile dökümantasyonlarınızı sorgulayın.")

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
