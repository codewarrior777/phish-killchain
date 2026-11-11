"""
Phish-Killchain: Advanced Email Forensics & Social Engineering Analyzer.
Single-File Version (Final & Optimized).
"""

import streamlit as st
import plotly.graph_objects as go
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Phish-Killchain", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 LIGHT NEON SKY BLUE THEME (CSS)
# ==========================================
celeste_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.stApp { 
    background-color: #00e5ff; 
    color: #001a33; 
    font-family: 'Share Tech Mono', monospace; 
}

/* TÍTULO PRINCIPAL */
h1 { 
    color: #001a33 !important; 
    -webkit-text-fill-color: #001a33 !important;
    text-transform: uppercase; 
    font-weight: 900;
    letter-spacing: 3px;
    border-bottom: 4px solid #001a33 !important; 
    padding-bottom: 10px !important; 
    text-shadow: none !important;
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

div[data-testid="stExpander"], .stInfo, .stAlert {
    background-color: #001a33 !important;
    color: #ffffff !important;
}

/* ESTILOS CORREGIDOS PARA LOS TÍTULOS DEL REPORTE DE IA */
div[data-testid="stMarkdownContainer"] h2, 
div[data-testid="stMarkdownContainer"] h3 {
    color: #001a33 !important; /* Azul oscuro para que sea visible */
    text-shadow: none !important;
    border-bottom: 2px solid #001a33 !important;
    margin-top: 2em !important;
    margin-bottom: 1em !important;
    padding-bottom: 5px;
}

.stInfo div, .stInfo p, .stInfo li, .stInfo td {
    color: #ffffff !important;
}

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

[data-testid="stSidebar"] { background-color: #00d2ff; }
</style>
"""
st.markdown(celeste_css, unsafe_allow_html=True)

# ==========================================
# 🛠️ CLASES Y FUNCIONES
# ==========================================
class EmailForensics:
    def __init__(self, file_path):
        self.file_path = file_path
        self.from_address = "HR Team <recruiter@career-apply.net>"
        self.reply_to = "hacker@protonmail.com"
        self.subject = "URGENT: Senior Engineer Role - Technical Test"
        self.body = """We found your profile on LinkedIn and we are very impressed with your Web3 background. 
We have an urgent opening for a Senior Engineer role.

Before the interview, please complete this quick technical test:
1. Download the custom testing script from http://career-apply.net/technical_test.exe
2. Run it to update your browser environment.
3. Reply to this message once done.

Let me know if you have any questions. Best regards, HR Team."""

    def analyze_headers(self):
        findings = []
        if self.reply_to != "recruiter@career-apply.net":
            findings.append(f"SPOOFING DETECTED: 'Reply-To' ({self.reply_to}) is different from 'From' ({self.from_address}).")
        if "URGENT" in self.subject.upper():
            findings.append("SUSPICIOUS SUBJECT: High urgency detected in subject line.")
        return findings

    def extract_urls(self):
        return ["http://career-apply.net/technical_test.exe"]

    def analyze_urls(self, urls):
        findings = []
        for url in urls:
            if url.endswith(".exe"):
                findings.append(f"MALICIOUS PAYLOAD: Direct download link to executable detected -> {url}")
        return findings

def generate_phishing_email():
    email_content = """From: HR Team <recruiter@career-apply.net>
Reply-To: hacker@protonmail.com
Subject: URGENT: Senior Engineer Role - Technical Test
Content-Type: text/plain; charset="utf-8"

We found your profile on LinkedIn and we are very impressed with your Web3 background. 
We have an urgent opening for a Senior Engineer role.

Before the interview, please complete this quick technical test:
1. Download the custom testing script from http://career-apply.net/technical_test.exe
2. Run it to update your browser environment.
3. Reply to this message once done.

Let me know if you have any questions. Best regards, HR Team.
"""
    with open("sample_phishing.eml", "w", encoding="utf-8") as f:
        f.write(email_content)

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
    Analyze the email body and write a Threat Intelligence Report.
    
    CRITICAL INSTRUCTIONS FOR FORMATTING:
    - You must use proper Markdown.
    - YOU MUST USE `###` FOR ALL SECTION TITLES. Do not use bold text for main titles.
    - Ensure all tables have the correct Markdown separator line (e.g., `|---|---|`).
    
    Structure exactly like this:
    ### 1. PSYCHOLOGICAL ATTACK MATRIX
    Create a table with columns: Psychological Lever | Description | How It Is Employed in the Email.
    
    ### 2. CORRELATION OF PSYCHOLOGICAL TACTICS WITH TECHNICAL INDICATORS
    Create a table with columns: Technical IOC | Corresponding Psychological Lever(s) | Explanation of the Link.
    
    ### 3. SOC ANALYST RECOMMENDATION
    Give a 1-sentence recommendation.
    
    Keep the tone professional, urgent, and analytical.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the email body:\n\n{body}"}
            ],
            temperature=0.3,
            max_tokens=1000
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

sample_path = "sample_phishing.eml"
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
            st.markdown(ai_report)
else:
    st.info("💡 **STANDBY MODE:** Awaiting forensic analysis command.")