import streamlit as st
from src.privacy import PrivacyShield
from src.engine import PolicyEngine

st.set_page_config(page_title="UIUC FERPA Shield Navigator", page_icon="🛡️")

@st.cache_resource
def load_systems():
    return PrivacyShield(), PolicyEngine()

shield , engine = load_systems()

st.title("🛡️ FERPA Shield Navigator")
st.markdown("Query UIUC student privacy policies safely and privately.")


user_query = st.text_input("Ask a policy question (e.g., 'Can I share my student's GPA with their parents?'):")

if user_query:
    with st.spinner("Anonymizing and searching..."):

        safe_query = shield.identify_and_mask(user_query)
        st.info(f"**Privacy Shield Active:** Searching for: *{safe_query}*")

        results = engine.search(safe_query)

        st.subheader("Relevant Policy Sections:")
        for i, doc in enumerate(results):
            with st.expander(f"Source {i+1}: {doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', '?')})"):
                st.write(doc.page_content)

st.sidebar.info("This prototype uses local embeddings to ensure zero data leakage.")
