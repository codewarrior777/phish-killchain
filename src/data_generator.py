import os

def generate_phishing_email():
    """Generates a synthetic .eml file for the demo mode."""
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
    # Guarda el archivo en la carpeta principal (un nivel arriba de src)
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_phishing.eml")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(email_content)
    print(f"Generated synthetic sample at {file_path}")