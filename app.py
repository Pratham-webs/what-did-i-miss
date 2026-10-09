import streamlit as st
import google.generativeai as genai
import os

# Page configuration
st.set_page_config(
    page_title="What Did I Miss? | ProtocolX",
    page_icon="⚡",
    layout="wide"
)

# Clear any system environment variables that could cause token conflicts
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("GEMINI_API_KEY", None)

# Sidebar setup
with st.sidebar:
    st.header("🔑 App Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.divider()
    st.caption("ProtocolX Challenge micro-app")

# Main Title & Subtitle
st.title("⚡ What Did I Miss?")
st.subheader("The Unread Problem Solver")
st.write("Extract and prioritize essential information from unread chat streams.")

# Two-column layout
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("#### 📥 Input Chat")
    chat_data = st.text_area(
        "Paste your chat conversation here:",
        height=320,
        placeholder="[10:15 AM] Alex: We need to submit the deck by 3 PM!\n[10:16 AM] Priya: Slides 1 to 5 are ready.\n[10:20 AM] Alex: Decision: keep it under 10 slides."
    )
    analyze_btn = st.button("🚀 Analyze Chat", type="primary", use_container_width=True)

with col_output:
    st.markdown("#### 📊 AI Prioritization")
    if analyze_btn:
        if not api_key.strip():
            st.error("👈 Please paste your Gemini API Key in the left sidebar.")
        elif not chat_data.strip():
            st.warning("Please paste chat text into the box on the left.")
        else:
            with st.spinner("Analyzing conversation with Gemini..."):
                try:
                    clean_key = api_key.strip()
                    genai.configure(api_key=clean_key)

                    # Using gemini-3.8-flash as required by the API
                    model = genai.GenerativeModel("gemini-3.8-flash")

                    prompt = f"""
                    You are an AI assistant designed to solve the "Unread Problem" for overwhelming chats.
                    Analyze the following conversation and produce a clean, structured output:

                    ### 📌 Executive Summary
                    A concise 2-sentence summary of what happened.

                    ### 🎯 Action Items & Decisions
                    - Key decisions made
                    - Tasks assigned and to whom

                    ### ⏰ Deadlines & Urgent Mentions
                    - Highlight any strict deadlines, time constraints, or urgent call-outs.

                    Chat Log:
                    {chat_data}
                    """

                    response = model.generate_content(prompt)
                    st.success("Analysis Complete!")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Error during generation: {e}")
    else:
        st.info("Paste your chat on the left and click 'Analyze Chat' to view insights.")