from email.header import Header
from email.mime.text import MIMEText
import smtplib


def send_email(smtp_server, from_email, from_pass, to_emails, email_subject, email_body):
    smtp_server = smtp_server

    msg = MIMEText(email_body, "plain", "utf-8")
    msg["From"] = Header(from_email)
    msg["To"] = Header(",".join(to_emails))
    msg["Subject"] = Header(email_subject)

    server = smtplib.SMTP(smtp_server, 587)
    server.ehlo()
    server.starttls()
    server.login(from_email, from_pass)
    server.sendmail(from_email, to_emails, msg.as_string())
    server.quit()
