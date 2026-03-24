import streamlit as st

def chat_message_html(role, content, sources=None):
    """WhatsApp/ChatGPT tarzı chat baloncukları oluşturur."""
    is_user = role == "user"
    bubble_class = "user-bubble" if is_user else "assistant-bubble"
    
    source_html = ""
    if sources:
        source_html = f'<span class="source-tag">📚 Kaynak: {", ".join(sources)}</span>'
        
    html = f"""
    <div style="display: flex; flex-direction: column;">
        <div class="bubble {bubble_class}">
            {content}
            {source_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def inject_styles():
    """Özel CSS dosyasını enjekte eder."""
    with open("frontend/assets/styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
