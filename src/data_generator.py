"""
Generates a synthetic malicious .eml file simulating a spear-phishing attack.
"""

import os
from email.message import EmailMessage

def generate_phishing_email():
    msg = EmailMessage()
    
    # --- HEADERS (El sobre del correo) ---
    msg['From'] = "HR Team <recruiter@career-apply.net>"
    msg['To'] = "engineer@binance.com"
    msg['Subject'] = "URGENT: Senior Engineer Role - Technical Test"
    # Un truco clásico: El Reply-To va a un correo distinto al From
    msg['Reply-To'] = "hacker@protonmail.com" 
    
    # --- BODY (El contenido que engaña al humano) ---
    body = """
    Hi there,

    We found your profile on LinkedIn and we are very impressed with your Web3 background. 
    We have an urgent opening for a Senior Engineer role.

    Before the interview, please complete this quick technical test:
    1. Download the custom testing script from http://career-apply.net/technical_test.exe
    2. Run it to update your browser environment.
    3. Reply to this message once done.

    Let me know if you have any questions. Best regards, HR Team.
    """
    msg.set_content(body)
    
    # Guardar como archivo .eml en la raíz
    filepath = os.path.join(os.path.dirname(__file__), "../sample_phishing.eml")
    with open(filepath, "wb") as f:
        f.write(msg.as_bytes())
        
    print(f"✅ Correo de phishing generado en: {filepath}")

if __name__ == "__main__":
    generate_phishing_email()