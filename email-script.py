import creds
import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def email_new(df):
    message = MIMEMultipart()
    message['Subject'] = "New Data from Today"
    message['From'] = creds.sender
    message['To'] = creds.recipient

    html = MIMEText(df.to_html(index=False), "html")
    message.attach(html)
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(creds.sender, creds.password)
        server.sendmail(creds.sender, creds.recipient, message.as_string())


def data_get():
    r = requests.get('https://rickandmortyapi.com/api/episode')
    episodes = pd.json_normalize(r.json()['results'])
    return episodes


if __name__ == '__main__':
    data = data_get()
    email_new(data)