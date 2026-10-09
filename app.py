import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="What Did I Miss?", layout="wide")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Gemini API Key:", type="password")

st.title("⚡ What Did I Miss?")
st.markdown("### Chat Intelligence Engine")

col1, col2 = st.columns(2)

with col1:
    chat_text = st.text_area("Paste Chat Log:", height=300, placeholder="Paste conversation here...")
    analyze = st.button("Run Analysis", type="primary")

with col2:
    st.markdown("### Output")
    if analyze:
        if not api_key:
            st.error("Please provide your API key in the sidebar.")
        elif not chat_text.strip():
            st.warning("Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    genai.configure(api_key=api_key.strip())
                    # Using the active, supported flash model endpoint
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    
                    prompt = f"""
                    Analyze the chat log below and extract:
                    1. Executive Summary
                    2. Action Items & Owners
                    3. Deadlines
                    
                    Chat Log:
                    {chat_text}
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("Done!")
                    st.markdown(response.text)
                    
                    st.download_button("Download Report", data=response.text, file_name="report.txt")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Awaiting input...")