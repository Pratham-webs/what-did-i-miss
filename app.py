import streamlit as st
import google.generativeai as genai
import os
import json
import pandas as pd
from datetime import datetime

# --- 1. PAGE & UI CONFIGURATION ---
st.set_page_config(page_title="ProtocolX | Context Engine", page_icon="💠", layout="wide")

# Advanced Enterprise CSS
st.markdown("""
    <style>
    /* Sleek Dark Theme Overrides */
    .stApp { background-color: #0B0E14; }
    .stTextArea textarea { 
        border-radius: 8px; 
        border: 1px solid #2A2E39; 
        background-color: #151A22; 
        color: #E2E8F0; 
        font-family: 'Fira Code', monospace; 
    }
    /* Gradient Primary Button */
    .stButton>button[kind="primary"] { 
        background: linear-gradient(90deg, #FF3366 0%, #FF9933 100%);
        color: white; 
        border-radius: 8px; 
        font-weight: 800; 
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button[kind="primary"]:hover { 
        transform: scale(1.02); 
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.4); 
    }
    /* Custom Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #151A22;
        border: 1px solid #2A2E39;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION & SETTINGS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=40)
    st.header("Engine Settings")
    api_key = st.text_input("Gemini API Key:", type="password")
    
    st.divider()
    st.markdown("### 🎛️ Advanced Controls")
    ai_temp = st.slider("Model Temperature (Creativity vs Strictness):", 0.0, 1.0, 0.1, 0.1)
    
    st.divider()
    st.markdown("### 🧪 Simulation Data")
    if st.button("Inject Severity 1 Incident", use_container_width=True):
        st.session_state["chat"] = "[02:15] SysAdmin: Database master node crashed. Failover failed.\n[02:18] DBA: Logs show corruption in table users_main.\n[02:22] VP Eng: We are down. ETA to restore from backup?\n[02:25] DBA: 45 mins. I am starting the AWS snapshot restore now.\n[02:30] VP Eng: PR team, draft an external status page update."

# --- 3. MAIN DASHBOARD ---
st.title("💠 ProtocolX: Executive Dashboard")
st.markdown("Automated Context Extraction via Gemini 2.0 JSON Engine")
st.divider()

col_input, col_output = st.columns([1, 1.5], gap="large")

# -- INPUT COLUMN --
with col_input:
    st.markdown("#### 📡 Intercepted Communications")
    chat_text = st.text_area(
        "Raw Data Stream:", 
        height=400, 
        value=st.session_state.get("chat", "")
    )
    analyze_btn = st.button("⚡ Process Intelligence", type="primary", use_container_width=True)

# -- OUTPUT COLUMN --
with col_output:
    st.markdown("#### 📊 Structured Intelligence")
    
    if analyze_btn:
        if not api_key:
            st.error("SYSTEM HALTED: Valid API Key required in sidebar.")
        elif len(chat_text) < 15:
            st.warning("SYSTEM HALTED: Insufficient data payload.")
        else:
            with st.spinner("Executing JSON structured extraction..."):
                try:
                    # 1. Configure the API
                    genai.configure(api_key=api_key.strip())
                    
                    # 2. Force JSON Output (The Enterprise Secret)
                    model = genai.GenerativeModel(
                        "gemini-2.0-flash",
                        generation_config=genai.GenerationConfig(
                            temperature=ai_temp,
                            response_mime_type="application/json" 
                        )
                    )
                    
                    # 3. Define the strict JSON Schema in the prompt
                    prompt = f"""
                    Analyze the following chat log and output the result STRICTLY as a JSON object with this exact schema:
                    {{
                        "urgency_score": <integer from 1 to 10>,
                        "executive_summary": "<string, max 2 sentences>",
                        "action_items": [
                            {{"owner": "<string>", "task": "<string>", "status": "Pending"}}
                        ],
                        "deadlines": [
                            {{"deadline": "<string>", "event": "<string>"}}
                        ]
                    }}
                    
                    Chat Log:
                    {chat_text}
                    """
                    
                    response = model.generate_content(prompt)
                    
                    # 4. Parse the JSON back into a Python Dictionary
                    intel_data = json.loads(response.text)
                    
                    # 5. Render Beautiful Native Streamlit Components
                    
                    # Top-level metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric(label="🔥 Urgency Score", value=f"{intel_data['urgency_score']} / 10")
                    m2.metric(label="🎯 Tasks Identified", value=len(intel_data.get('action_items', [])))
                    m3.metric(label="⏰ Deadlines Found", value=len(intel_data.get('deadlines', [])))
                    
                    st.divider()
                    
                    # Executive Summary Box
                    st.info(f"**📌 Executive Summary:**\n{intel_data['executive_summary']}")
                    
                    # Interactive Action Items Table
                    st.markdown("#### 🛠️ Action Items Protocol")
                    if intel_data.get('action_items'):
                        df_actions = pd.DataFrame(intel_data['action_items'])
                        st.dataframe(df_actions, use_container_width=True, hide_index=True)
                    else:
                        st.write("No explicit action items assigned.")
                        
                    # Deadlines 
                    st.markdown("#### ⏳ Critical Timelines")
                    if intel_data.get('deadlines'):
                        for d in intel_data['deadlines']:
                            st.warning(f"**{d['deadline']}**: {d['event']}")
                    else:
                        st.write("No strict deadlines detected.")

                    # Export button for the raw JSON payload
                    st.download_button(
                        label="💾 Download Raw JSON Data",
                        data=json.dumps(intel_data, indent=4),
                        file_name=f"ProtocolX_Payload_{datetime.now().strftime('%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )

                except json.JSONDecodeError:
                    st.error("Data Parsing Error: The AI failed to return valid JSON formatting.")
                except Exception as e:
                    st.error(f"Critical System Failure: {e}")
    else:
        st.caption("Awaiting transmission. Inject data to visualize the JSON extraction engine.")