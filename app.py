import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ProtocolX: What Did I Miss?",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clear environment variables to prevent auth conflicts
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("GEMINI_API_KEY", None)

# --- PREMIUM UI/UX STYLING ---
st.markdown("""
    <style>
    .stTextArea textarea { 
        border-radius: 10px; 
        border: 1px solid #444; 
        font-family: 'Courier New', Courier, monospace; 
        background-color: #0e1117;
        color: #e0e0e0;
    }
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
    .report-box { 
        padding: 25px; 
        border-radius: 10px; 
        border: 1px solid #333; 
        background-color: #161a24; 
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("🔐 System Auth")
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="Enter key to unlock...")
    st.caption("Secured locally in your session memory.")
    st.divider()
    
    st.markdown("### 🧪 Quick Inject Data")
    st.caption("Instantly load sample crisis chat logs for testing.")
    
    sample_crisis = (
        "[10:00] Sarah (Product): Payment gateway API is throwing 500 errors in production.\n"
        "[10:02] Mark (DevOps): Investigating now. Looks like the SSL certificate expired at midnight.\n"
        "[10:05] Sarah (Product): We are losing customer transactions. What is our fix ETA?\n"
        "[10:08] Mark (DevOps): Generating new certificate. Will deploy hotfix by 10:30 AM.\n"
        "[10:10] David (Legal): Ensure we log downtime metrics per our SLA agreement."
    )
    
    if st.button("Inject Critical Log"):
        st.session_state["chat_input"] = sample_crisis

# --- MAIN APP HEADER ---
st.title("⚡ ProtocolX: Context Engine")
st.markdown("### The Unread Chat Intelligence & Priority Extraction System")
st.divider()

# --- MAIN DUAL-COLUMN LAYOUT ---
col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    with st.container(border=True):
        st.markdown("### 📡 Raw Communications Intercept")
        chat_text = st.text_area(
            "Stream Input:",
            value=st.session_state.get("chat_input", ""),
            height=360,
            placeholder="Paste raw chat messages or load preset from sidebar..."
        )
        run_analysis = st.button("⚡ Initialize Analysis", use_container_width=True)

with col_out:
    with st.container(border=True):
        st.markdown("### 🎯 Processed Intelligence")
        
        if run_analysis:
            clean_key = api_key.strip() if api_key else ""
            input_data = chat_text.strip()
            
            if not clean_key:
                st.error("⚠️ Access Denied: Please provide your Gemini API Key in the sidebar.")
            elif not input_data:
                st.warning("⚠️ Empty Stream: Please provide conversation text to analyze.")
            elif len(input_data) < 10:
                st.warning("⚠️ Input too short to extract meaningful context.")
            else:
                with st.spinner("Decrypting context, mapping priorities, and isolating deadlines..."):
                    try:
                        # Configure API with robust flash model
                        genai.configure(api_key=clean_key)
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        
                        prompt = f"""
                        You are an elite operational intelligence assistant. Analyze the conversation stream below to solve the "Unread Chat Problem".

                        STRICT RULES:
                        1. NO HALLUCINATION: Only include facts explicitly agreed upon in the text.
                        2. OBJECTIVE FORMATTING: Follow the markdown structure below precisely.

                        REQUIRED OUTPUT FORMAT:
                        ### 📌 Executive Summary
                        [2 sentences max summarizing the core situation]

                        ### 🚨 Critical Risks & Blockers
                        * [Bullet points of blockers/risks. If none, write "None identified."]

                        ### 🎯 Action Items & Ownership
                        * **[Owner Name]**: [Specific task or deliverable assigned]

                        ### ⏰ Deadlines & Timeline
                        * **[Time/Date]** — [Milestone or deadline expectation]

                        CONVERSATION LOG:
                        {input_data}
                        """
                        
                        response = model.generate_content(
                            prompt,
                            generation_config=genai.types.GenerationConfig(temperature=0.0)
                        )
                        
                        st.toast("Intelligence Extracted Successfully!", icon="✅")
                        
                        # Tabbed interface for reporting & downloading
                        tab_report, tab_export = st.tabs(["📑 Executive Report", "💾 Export Data"])
                        
                        with tab_report:
                            st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                            
                        with tab_export:
                            st.info("Securely download your intelligence briefing for offline review.")
                            st.download_button(
                                label="⬇️ Download Final Report (.txt)",
                                data=response.text,
                                file_name=f"ProtocolX_Intel_{datetime.now().strftime('%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                            
                    except Exception as err:
                        st.error(f"System Failure: {err}")
        else:
            st.info("System standing by. Provide chat data and click **'Initialize Analysis'**.")