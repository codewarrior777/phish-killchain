import email
from email import policy
import re

class EmailForensics:
    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            self.msg = email.message_from_binary_file(f, policy=policy.default)
            
        self.from_address = self.msg.get('From', 'Unknown')
        self.reply_to = self.msg.get('Reply-To', 'Unknown')
        self.subject = self.msg.get('Subject', 'Unknown')
        self.body = self._get_body()
        
    def _get_body(self):
        if self.msg.is_multipart():
            for part in self.msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_content()
        else:
            return self.msg.get_content()
        return ""

    def analyze_headers(self):
        findings = []
        if self.reply_to != 'Unknown' and self.reply_to != self.from_address:
            findings.append(f"⚠️ SPOOFING DETECTED: 'Reply-To' ({self.reply_to}) is different from 'From' ({self.from_address}).")
            
        if "urgent" in self.subject.lower() or "test" in self.subject.lower():
            findings.append(f"⚠️ SUSPICIOUS SUBJECT: High urgency detected in subject line.")
            
        return findings

    def extract_urls(self):
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        return re.findall(url_pattern, self.body)
        
    def analyze_urls(self, urls):
        findings = []
        suspicious_exts = ['.exe', '.bat', '.scr', '.vbs']
        
        for url in urls:
            if any(url.lower().endswith(ext) for ext in suspicious_exts):
                findings.append(f"🚨 MALICIOUS PAYLOAD: Direct download link to executable detected -> {url}")
            elif "career-apply" in url or "login" in url:
                findings.append(f"⚠️ SUSPICIOUS DOMAIN: Lookalike or known malicious domain -> {url}")
                
        return findings