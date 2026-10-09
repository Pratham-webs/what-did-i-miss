import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Intel Engine | ProtocolX", page_icon="💠", layout="wide")

os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("GEMINI_API_KEY", None)

# --- PREMIUM UI CSS ---
st.markdown("""
    <style>
    /* Styling the text area to look like a terminal */
    .stTextArea textarea { 
        border-radius: 10px; 
        border: 1px solid #444; 
        font-family: 'Courier New', Courier, monospace; 
        background-color: #0e1117;
    }
    /* Glowing Gradient Button */
    .stButton>button { 
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white; 
        border-radius: 8px; 
        font-weight: 800; 
        text-transform: uppercase; 
        letter-spacing: 1px;
        transition: all 0.3s ease; 
        border: none; 
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
    }
    .stButton>button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 6px 20px rgba(255, 65, 108, 0.6); 
    }
    /* Custom Output Box */
    .report-box { 
        padding: 25px; 
        border-radius: 10px; 
        border: 1px solid #333; 
        background-color: #161a24; 
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR AUTHENTICATION ---
with st.sidebar:
    st.header("🔐 System Auth")
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="Enter key to unlock...")
    st.divider()
    
    st.markdown("### 🧪 Quick Inject Data")
    st.caption("Test the UI instantly with pre-configured crisis data.")
    sample_data = (
        "[10:00] Sarah (Product): API is throwing 500 errors in production.\n"
        "[10:02] Mark (DevOps): Investigating. SSL expired at midnight.\n"
        "[10:05] Sarah (Product): Losing $500/min. Fix ETA?\n"
        "[10:08] Mark (DevOps): Generating new cert. Deploy by 10:30 AM.\n"
        "[10:10] David (Legal): Notify users about the downtime per our SLA."
    )
    if st.button("Inject Critical Log"):
        st.session_state["chat_input"] = sample_data

# --- HEADER ---
st.title("💠 ProtocolX: Context Engine")
st.markdown("#### Enterprise-Grade Communication Distillation")

# --- SPLIT LAYOUT WITH CONTAINERS ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 📡 Raw Intercept")
        chat_text = st.text_area(
            "Stream Input:", 
            value=st.session_state.get("chat_input", ""), 
            height=350,
            placeholder="Awaiting data transmission..."
        )
        run_analysis = st.button("⚡ Initialize Analysis", use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("### 🎯 Processed Intelligence")
        if run_analysis:
            if not api_key:
                st.error("Access Denied: API Key required in sidebar.")
            elif len(chat_text.strip()) < 10:
                st.warning("Insufficient data stream to process.")
            else:
                with st.spinner("Decrypting context and mapping priorities..."):
                    try:
                        genai.configure(api_key=api_key.strip())
                        # Switched to gemini-1.5-flash to bypass rate limits
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        prompt = f"""
                        You are an elite operational AI. Process this chat log and extract objective facts.
                        FORMAT EXACTLY AS FOLLOWS USING MARKDOWN:
                        
                        ### 📌 Executive Summary
                        [2 sentences max summarizing the core issue]
                        
                        ### 🚨 Critical Risks
                        * [Bullet points of blockers/risks]
                        
                        ### 🛠️ Action Protocol
                        * **[Owner]** - [Task] (Deadline: [Time/Date if mentioned])
                        
                        RAW LOG:
                        {chat_text}
                        """
                        
                        response = model.generate_content(
                            prompt, 
                            generation_config=genai.types.GenerationConfig(temperature=0.0)
                        )
                        
                        st.toast("Intelligence Extracted Successfully!", icon="✅")
                        
                        tab1, tab2 = st.tabs(["📑 Executive Report", "💾 Export Data"])
                        with tab1:
                            st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                        with tab2:
                            st.info("Securely download this intelligence briefing for offline review.")
                            st.download_button(
                                "⬇️ Download Final Report (.txt)", 
                                data=response.text, 
                                file_name=f"Intel_{datetime.now().strftime('%H%M%S')}.txt", 
                                use_container_width=True
                            )
                            
                    except Exception as err:
                        st.error(f"System Failure: {err}")
        else:
            st.info("Awaiting command sequence. Inject data and initialize.")