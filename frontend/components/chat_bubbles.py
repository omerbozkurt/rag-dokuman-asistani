import streamlit as st

def chat_message_html(role, content, sources=None):
    """Modern ve şık chat baloncukları oluşturur."""
    is_user = role == "user"
    bubble_class = "user-bubble" if is_user else "assistant-bubble"
    label_class = "user-label" if is_user else "assistant-label"
    label_text = "SİZ" if is_user else "ASİSTAN"
    icon = "👤" if is_user else "🤖"
    
    source_html = ""
    if sources:
        source_html = f'<div class="source-tag">📚 Kaynaklar: {", ".join(sources)}</div>'
        
    html = f"""
    <div style="display: flex; flex-direction: column; width: 100%; align-items: {'flex-end' if is_user else 'flex-start'};">
        <div class="role-label" style="text-align: {'right' if is_user else 'left'};">
            {icon if not is_user else ""} {label_text} {icon if is_user else ""}
        </div>
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
