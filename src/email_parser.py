class EmailForensics:
    def __init__(self, file_path):
        self.file_path = file_path
        
        # Datos simulados que coinciden con tu captura de pantalla
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
        # En una app real usarías regex, aquí simulamos la extracción
        return ["http://career-apply.net/technical_test.exe"]

    def analyze_urls(self, urls):
        findings = []
        for url in urls:
            if url.endswith(".exe"):
                findings.append(f"MALICIOUS PAYLOAD: Direct download link to executable detected -> {url}")
        return findings