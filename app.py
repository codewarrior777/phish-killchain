"""
Phish-Killchain: Advanced Email Forensics & Social Engineering Analyzer.
Ultimate Light Neon Sky Blue Theme.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time
from openai import OpenAI
from src.email_parser import EmailForensics
from src.data_generator import generate_phishing_email
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Phish-Killchain", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 LIGHT NEON SKY BLUE THEME (CSS)
# ==========================================
celeste_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Fondo general en Celeste Neón Brillante */
.stApp { 
    background-color: #00e5ff; 
    color: #001a33; 
    font-family: 'Share Tech Mono', monospace; 
}

h1 { 
    color: #001a33 !important; 
    text-transform: uppercase; 
    font-weight: 900;
    letter-spacing: 3px;
    border-bottom: 4px solid #001a33; 
    padding-bottom: 10px; 
    text-shadow: 3px 3px 0px #ffffff, 0 0 20px rgba(255, 255, 255, 0.4); 
}

h2, h3 { 
    color: #003366 !important; 
    text-transform: uppercase; 
    font-weight: bold;
}

.stButton > button { 
    background-color: #ffffff !important; 
    color: #001a33 !important; 
    border: 3px solid #001a33 !important; 
    border-radius: 0px !important; 
    text-transform: uppercase; 
    font-weight: 900; 
    letter-spacing: 1px;
    width: 100%; 
    transition: all 0.3s; 
}
.stButton > button:hover { 
    background-color: #001a33 !important; 
    color: #00e5ff !important; 
    box-shadow: 0 0 20px rgba(0, 26, 51, 0.8); 
}

div[data-testid="stMetric"] { 
    background-color: #ffffff; 
    border: 2px solid #001a33; 
    border-left: 8px solid #001a33; 
    padding: 15px; 
}
div[data-testid="stMetricValue"] { 
    color: #001a33 !important; 
    font-weight: 900;
}

.terminal-window { 
    background-color: #001a33; 
    border: 2px solid #001a33; 
    padding: 15px; 
    height: 250px; 
    overflow-y: auto; 
    font-size: 13px; 
    color: #00e5ff; 
    box-shadow: inset 0 0 15px rgba(0, 229, 255, 0.3);
}

/* --- ESTILOS PARA EL REPORTE DE IA (Nativo de Streamlit) --- */
div[data-testid="stExpander"], .stInfo, .stAlert {
    background-color: #001a33 !important;
    color: #ffffff !important;
}

/* Títulos dentro de las tablas y el reporte */
div[data-testid="stMarkdownContainer"] h1, 
div[data-testid="stMarkdownContainer"] h2, 
div[data-testid="stMarkdownContainer"] h3 {
    color: #00e5ff !important;
    text-shadow: 0 0 5px rgba(0, 229, 255, 0.5);
}

/* Forzar que el texto generado por la IA sea blanco para que contraste con el fondo oscuro */
.stInfo div, .stInfo p, .stInfo li, .stInfo td {
    color: #ffffff !important;
}

/* Estilo para las tablas de la IA (Markdown) */
table {
    background-color: #001a33 !important;
    color: #ffffff !important;
    border-collapse: collapse;
    width: 100%;
}
th {
    background-color: #00e5ff !important;
    color: #001a33 !important;
    font-weight: bold;
    padding: 10px;
    border: 1px solid #001a33;
}
td {
    border: 1px solid #00e5ff !important;
    padding: 10px;
}

[data-testid="stSidebar"] {
    background-color: #00d2ff;
}
</style>
"""
st.markdown(celeste_css, unsafe_allow_html=True)

# ==========================================
# AI CLIENT (Groq)
# ==========================================
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY", "dummy_key")
)
MODEL = "openai/gpt-oss-120b" 

def generate_ai_analysis(body, technical_findings):
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "dummy_key":
        return "⚠️ AI Analysis disabled. Missing GROQ_API_KEY in .env."
        
    findings_text = "\n".join(technical_findings) if technical_findings else "No technical IOCs found."
    
    system_prompt = f"""
    You are a Senior Threat Intelligence Analyst specializing in Social Engineering and Phishing.
    We have intercepted an email. Our technical scanner found these indicators of compromise (IOCs):
    
    {findings_text}
    
    Your Task:
    Analyze the email body and write a Threat Intelligence Report:
    1. Explain the psychology of the attack (e.g., authority, urgency, fear). Use a table to map tactics.
    2. Link the psychological tactics to the technical findings. Use another table for this correlation.
    3. Give a 1-sentence recommendation for SOC analysts.
    
    Keep the tone professional, urgent, and analytical. Use Markdown.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the email body:\n\n{body}"}
            ],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ AI Analysis failed: {str(e)}"

# ==========================================
# HEADER
# ==========================================
st.title("🛡️ PHISH-KILLCHAIN // THREAT FORENSICS")
st.markdown("**Advanced Social Engineering & Threat Intelligence Analyzer**")

st.sidebar.warning("⚠️ **RESTRICTED SYSTEM**\n\nThis tool is for defensive security analysis. Never upload real sensitive emails. Use the synthetic sample provided.")

sample_path = os.path.join(os.path.dirname(__file__), "sample_phishing.eml")
if not os.path.exists(sample_path):
    generate_phishing_email()

uploaded_file = st.sidebar.file_uploader("Upload Suspicious Email (.eml)", type=["eml"])

if uploaded_file is not None:
    file_to_analyze = uploaded_file
    st.sidebar.success("File uploaded successfully.")
else:
    file_to_analyze = sample_path
    st.info("💡 **Demo Mode:** Using synthetic TraderTraitor phishing sample. Upload your own `.eml` to test.")

st.divider()

# ==========================================
# MAIN ANALYSIS
# ==========================================
if st.button("🚀 INITIATE FORENSIC ANALYSIS", type="primary"):
    with st.spinner("Parsing headers and extracting IOCs..."):
        time.sleep(0.5)
        
        parser = EmailForensics(file_to_analyze)
        header_findings = parser.analyze_headers()
        urls = parser.extract_urls()
        url_findings = parser.analyze_urls(urls)
        all_findings = header_findings + url_findings
        
        threat_score = 0
        if header_findings: threat_score += 40
        if url_findings: threat_score += 50
        if threat_score > 100: threat_score = 100
        
        col1, col2 = st.columns([1, 1.5], gap="large")
        
        with col1:
            st.markdown("### 📧 EMAIL HEADERS")
            st.markdown(f"**From:** `{parser.from_address}`")
            st.markdown(f"**Reply-To:** `{parser.reply_to}`")
            st.markdown(f"**Subject:** `{parser.subject}`")
            
            gauge_color = "#ff003c" if threat_score > 50 else "#001a33"
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = threat_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "THREAT SCORE", 'font': {'color': '#001a33', 'size': 18, 'family': 'Share Tech Mono'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "#001a33", 'tickfont': {'color': '#001a33'}},
                    'bar': {'color': gauge_color}, 
                    'bgcolor': "#ffffff",
                    'borderwidth': 3, 'bordercolor': "#001a33",
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(0, 26, 51, 0.1)'},
                        {'range': [40, 70], 'color': 'rgba(255, 193, 7, 0.2)'},
                        {'range': [70, 100], 'color': 'rgba(255, 0, 60, 0.2)'}],
                }
            ))
            fig.update_layout(paper_bgcolor="#00e5ff", height=220, margin=dict(l=20, r=20, t=40, b=10))
            st.plotly_chart(fig, width="stretch", key="gauge_chart")
            
        with col2:
            st.markdown("### 🚨 TECHNICAL IOCs DETECTED")
            if all_findings:
                for finding in all_findings:
                    st.error(finding)
            else:
                st.success("✅ No immediate technical IOCs detected.")
                
            st.markdown("### 📜 RAW EMAIL BODY")
            formatted_body = parser.body.replace('\n', '<br>')
            st.markdown(f'<div class="terminal-window">{formatted_body}</div>', unsafe_allow_html=True)

        st.divider()
        
        st.markdown("### 🧠 AUTOMATED THREAT PSYCHOLOGY REPORT")
        
        with st.spinner("Threat Intel AI is analyzing the psychological tactics..."):
            ai_report = generate_ai_analysis(parser.body, all_findings)
            # EL FIX ESTÁ AQUÍ: Usamos st.info() o st.markdown() nativo en lugar de envolverlo en HTML puro
            # para que Streamlit procese correctamente las tablas de Markdown.
            st.info(ai_report)
else:
    st.info("💡 **STANDBY MODE:** Awaiting forensic analysis command.")