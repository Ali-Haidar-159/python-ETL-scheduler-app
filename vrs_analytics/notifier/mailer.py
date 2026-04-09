import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

sender_email = "alihaidar379227@gmail.com"
receiver_email = "stylessboy0123@gmail.com"

app_pass = os.getenv("MAIL_APP_PASS")

def send_email(message) :
    text = f"Subject: ETL-data\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    server.login(sender_email,app_pass)
    server.sendmail(sender_email,receiver_email,text)

    print("Email send successfully")