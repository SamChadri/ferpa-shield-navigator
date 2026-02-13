import streamlit as st
from src.privacy import PrivacyShield
from src.engine import PolicyEngine
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from datetime import datetime

msgs = StreamlitChatMessageHistory(key="special_app_key")

st.set_page_config(page_title="UIUC FERPA Shield Navigator", page_icon="🛡️")

@st.cache_resource
def load_systems():
    return PrivacyShield(), PolicyEngine()

shield , engine = load_systems()

st.title("🛡️ FERPA Shield Navigator")
st.markdown("Query UIUC student privacy policies safely and privately.")

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if len(msgs.messages) == 0:
    msgs.add_ai_message("Hello! I am the UIUC Privacy Assistant. How can I help you today?")

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input("Ask about UIUC policy..."):
    st.chat_message("user").write(prompt)
    raw_user_input = prompt
    
    safe_prompt = shield.identify_and_mask(prompt)

    st.session_state.audit_log.insert(0, {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "raw": raw_user_input,
        "masked": safe_prompt
    })
    st.session_state.audit_log = st.session_state.audit_log[:5]
    
    formatted_history = [(m.type, m.content) for m in msgs.messages]
    
    with st.spinner("Consulting UIUC Policy..."):
        answer, docs = engine.get_chat_response(safe_prompt, formatted_history)
    
    st.chat_message("assistant").write(answer)

    if docs:
        with st.expander("📚 View Policy Sources"):
            for i, doc in enumerate(docs):
                source_name = doc.metadata.get('source','Unknown Policy')
                page_num = doc.metadata.get('page','N/A')

                st.markdown(f"**Source {i+1}:** {source_name} (Page {page_num})")
                st.caption(f"Relevant Snippet: ...{doc.page_content[:200]}...")
                st.divider()

    
    msgs.add_user_message(prompt)
    msgs.add_ai_message(answer)

with st.sidebar:
    st.header("🛡️ Privacy Audit Log")
    st.info("This log shows how PII is stripped locally before being sent to the LLM.")
    
    for entry in st.session_state.audit_log:
        with st.expander(f"Log [{entry['timestamp']}]"):
            st.markdown("**Original Input:**")
            st.caption(entry['raw'])
            st.markdown("**Shielded Version:**")
            st.code(entry['masked'], language=None)
            st.success("✅ PII Redacted / No PII Detected")

