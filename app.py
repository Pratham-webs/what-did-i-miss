import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="What Did I Miss? | ProtocolX", page_icon="⚡", layout="wide")

os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("GEMINI_API_KEY", None)

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 6px; font-family: monospace; font-size: 13px; }
    .stButton>button { border-radius: 6px; font-weight: bold; transition: all 0.2s ease; }
    .stButton>button:hover { transform: scale(1.02); }
    .report-header { color: #ff4b4b; font-weight: 800; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR & AUTHENTICATION ---
with st.sidebar:
    st.header("🔑 System Auth")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.divider()
    
    st.markdown("### 🧪 Simulation Data")
    sample_data = (
        "[10:00] Sarah (Product): The payment gateway API is throwing 500 errors in production.\n"
        "[10:02] Mark (DevOps): Investigating. Looks like the SSL certificate expired at midnight.\n"
        "[10:05] Sarah (Product): We are losing $500/minute. When can this be fixed?\n"
        "[10:08] Mark (DevOps): I am generating a new cert now. Will deploy by 10:30 AM.\n"
        "[10:10] David (Legal): Ensure we notify users about the downtime per our SLA."
    )
    if st.button("Load Critical Incident Log"):
        st.session_state["chat_input"] = sample_data

# --- HEADER ---
st.title("⚡ What Did I Miss? v3.0")
st.markdown("### Enterprise Context Extraction Engine")

# --- MAIN LAYOUT ---
col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown("#### 📥 Communications Stream")
    default_val = st.session_state.get("chat_input", "")
    chat_text = st.text_area(
        "Raw chat logs:",
        value=default_val,
        height=400,
        placeholder="Paste conversation data here..."
    )
    run_analysis = st.button("🧠 Execute Advanced Analysis", type="primary", use_container_width=True)

with col_out:
    st.markdown("#### 📊 Tactical Dashboard")
    
    if run_analysis:
        if not api_key.strip():
            st.error("⚠️ Authentication Required: Please input your Gemini API Key in the sidebar.")
        elif len(chat_data := chat_text.strip()) < 15:
            st.warning("⚠️ Insufficient Data: The input text is too short to analyze.")
        else:
            with st.spinner("Applying strict parsing protocols and extracting data..."):
                try:
                    genai.configure(api_key=api_key.strip())
                    model = genai.GenerativeModel("gemini-3.8-flash")
                    
                    # --- ADVANCED PROMPT ENGINEERING (v3.0) ---
                    prompt = f"""
You are a highly analytical Chief Operating Officer. Your task is to process the following raw chat log and extract purely objective, actionable intelligence.

CRITICAL INSTRUCTIONS:
1. NO HALLUCINATION: Only include information explicitly stated in the text.
2. NO CHIT-CHAT: Do not include conversational responses (e.g., "Here is the summary"). Output the exact Markdown structure below and nothing else.
3. EDGE CASE PROTOCOL: If the input text is random characters (e.g., "asdfgh"), output ONLY: "⚠️ **SYSTEM ERROR: Invalid communication stream detected. No actionable data.**"

REQUIRED OUTPUT STRUCTURE:
<div class="report-header">INTEL REPORT: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>

**🔥 OVERALL URGENCY SCORE: [Rate 1 to 10 based on context]**

### 📌 1. Situation Brief
[Max 2 sentences summarizing the core issue or topic.]

### 🚨 2. Blockers & Risks
* [List any identified blockers, errors, or risks. If none, state "No explicit risks identified."]

### 🎯 3. Action Items & Owners
* **[Name/Owner]**: [Specific task]

### ⏰ 4. Hard Deadlines
* **[Time/Date]** - [Deliverable]

---
RAW LOG TO PROCESS:
{chat_data}
"""
                    
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.0, # Zero creativity, maximum precision
                            max_output_tokens=500
                        )
                    )
                    
                    # Create Tabs for better UI
                    tab1, tab2 = st.tabs(["📝 Formatted Report", "📋 Raw Output"])
                    
                    with tab1:
                        st.markdown(response.text, unsafe_allow_html=True)
                        st.divider()
                        # Export Feature for extra hackathon points
                        st.download_button(
                            label="💾 Download Intelligence Report (TXT)",
                            data=response.text,
                            file_name=f"intel_report_{datetime.now().strftime('%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        
                    with tab2:
                        st.text(response.text)
                        
                except Exception as err:
                    st.error(f"Execution Error: {err}")
    else:
        st.info("System standing by. Provide chat data and execute analysis.")