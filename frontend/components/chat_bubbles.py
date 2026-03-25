import streamlit as st

def chat_message_html(role, content, sources=None):
    """Modern ve şık chat baloncukları oluşturur."""
    is_user = role == "user"
    bubble_class = "user-bubble" if is_user else "assistant-bubble"
    
    # SVG İkonları
    user_icon = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>"""
    bot_icon = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>"""
    
    icon = user_icon if is_user else bot_icon
    label_text = "SİZ" if is_user else "DOKÜMAN ASİSTANI"
    
    source_html = ""
    if sources:
        source_tags = "".join([f'<div class="source-tag">{s}</div>' for s in sources])
        source_html = f'<div class="source-container">{source_tags}</div>'
        
    html = f"""<div style="display: flex; flex-direction: column; width: 100%; align-items: {"flex-end" if is_user else "flex-start"}; margin-bottom: 2rem;">
<div style="display: flex; align-items: center; margin-bottom: 8px; font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); letter-spacing: 0.05em; text-transform: uppercase;">
{icon if not is_user else ""} {label_text} {icon if is_user else ""}
</div>
<div class="bubble {bubble_class}">
<div style="line-height: 1.6;">{content}</div>
{source_html}
</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)

def inject_styles():
    """Özel CSS dosyasını enjekte eder."""
    try:
        with open("frontend/assets/styles.css", "r", encoding="utf-8") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS dosyası bulunamadı!")
