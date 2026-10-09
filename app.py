import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="What Did I Miss? | ProtocolX",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clear environment variables to prevent auth conflicts
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("GEMINI_API_KEY", None)

# --- PROFESSIONAL STYLING (UI/UX WEIGHTAGE) ---
st.markdown("""
    <style>
    .stTextArea textarea { 
        border-radius: 8px; 
        border: 1px solid #333; 
        font-family: 'Courier New', Courier, monospace; 
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stButton>button { 
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white; 
        border-radius: 8px; 
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
        border: none; 
        box-shadow: 0 4px 12px rgba(255, 65, 108, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover { 
        transform: translateY(-1px); 
        box-shadow: 0 6px 16px rgba(255, 65, 108, 0.5); 
    }
    .report-card { 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #262730; 
        background-color: #161922; 
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("🔐 System Auth")
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="Enter API key...")
    st.caption("Secured locally in session memory.")
    st.divider()
    
    st.markdown("### 🧪 Quick Inject Preset")
    st.caption("Instantly load sample crisis data for testing.")
    
    sample_crisis = (
        "[10:00] Sarah (Product): Payment gateway API is throwing 500 errors in production.\n"
        "[10:02] Mark (DevOps): Investigating now. Looks like the SSL certificate expired at midnight.\n"
        "[10:05] Sarah (Product): We are losing customer transactions. What is our fix ETA?\n"
        "[10:08] Mark (DevOps): Generating new certificate. Will deploy hotfix by 10:30 AM.\n"
        "[10:10] David (Legal): Ensure we log downtime metrics per our SLA agreement."
    )
    
    if st.button("Load Crisis Log"):
        st.session_state["chat_input"] = sample_crisis

# --- MAIN APP HEADER ---
st.title("⚡ What Did I Miss?")
st.markdown("##### Enterprise Context & Priority Extraction Engine")
st.divider()

# --- DUAL COLUMN LAYOUT ---
col_left, col_right = st.columns([1, 1.1], gap="large")

with col_left:
    with st.container(border=True):
        st.markdown("### 📥 Raw Communications Stream")
        chat_text = st.text_area(
            "Paste conversation logs below:",
            value=st.session_state.get("chat_input", ""),
            height=360,
            placeholder="Paste chat messages here or use sidebar preset..."
        )
        analyze_btn = st.button("🚀 Initialize Analysis", use_container_width=True)

with col_right:
    with st.container(border=True):
        st.markdown("### 📊 Processed Intelligence")
        
        if analyze_btn:
            clean_key = api_key.strip() if api_key else ""
            input_data = chat_text.strip()
            
            if not clean_key:
                st.error("⚠️ Authentication Error: Please provide your Gemini API Key in the sidebar.")
            elif not input_data:
                st.warning("⚠️ Empty Stream: Please provide chat text to analyze.")
            elif len(input_data) < 10:
                st.warning("⚠️ Input too short for meaningful context extraction.")
            else:
                with st.spinner("Executing semantic extraction & priority mapping..."):
                    try:
                        # Configure API and use stable flash model
                        genai.configure(api_key=clean_key)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        prompt = f"""
                        You are an elite operational intelligence assistant. Analyze the conversation stream below to solve the "Unread Chat Problem".

                        STRICT RULES:
                        1. Be objective and factual based solely on the text.
                        2. Format output cleanly using the exact markdown structure requested below.

                        REQUIRED OUTPUT FORMAT:
                        ### 📌 Executive Summary
                        [2 sentences max summarizing the core situation]

                        ### 🚨 Critical Risks & Blockers
                        * [Bullet points of key blockers or risks. If none, write "None identified."]

                        ### 🎯 Action Items & Owners
                        * **[Owner Name]**: [Specific task or deliverable]

                        ### ⏰ Deadlines & Timeline
                        * **[Time/Date]** — [Milestone or deadline]

                        CONVERSATION LOG:
                        {input_data}
                        """
                        
                        response = model.generate_content(
                            prompt,
                            generation_config=genai.types.GenerationConfig(temperature=0.1)
                        )
                        
                        st.toast("Analysis completed successfully!", icon="✅")
                        
                        # Render output with clean tabs
                        tab_rep, tab_exp = st.tabs(["📑 Report View", "💾 Export Data"])
                        
                        with tab_rep:
                            st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                            
                        with tab_exp:
                            st.info("Download your structured intelligence report.")
                            st.download_button(
                                label="⬇️ Download Report (.txt)",
                                data=response.text,
                                file_name=f"Intel_Report_{datetime.now().strftime('%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                            
                    except Exception as err:
                        st.error(f"Execution Error: {err}")
        else:
                        st.info("System standing by. Provide input data and click **'Initialize Analysis'**.")