import smtplib
from email.mime.text import MIMEText

class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_notification(self, to_email, subject, message):
        print("\n" + "="*40)
        print(f"Sending notification to {to_email}: {subject} - {message}")
        print("="*40 + "\n")
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = to_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail('smtp@mailtrap.io', to_email, msg.as_string())
