import streamlit as st
import requests

st.set_page_config(page_title="Codebase Genius", page_icon="📚")
st.title("📚 Codebase Genius")
st.markdown("AI-powered code documentation system")

repo_url = st.text_input("Enter GitHub Repository URL:", placeholder="https://github.com/username/repo")

if st.button("Generate Documentation"):
    if repo_url:
        st.info(f"Backend integration coming soon for: {repo_url}")
    else:
        st.warning("Please enter a GitHub repository URL")
