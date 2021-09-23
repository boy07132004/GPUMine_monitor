from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json


with open("config.json") as f:
    emailAccount = json.load(f)['mailAccount']
    sender = emailAccount['sender']
    password = emailAccount['applicationPassword']
    recipients = emailAccount['recipients']

def send_warining_email(miner = "Miner name", worker = "Worker name", url = ""):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = f"{miner} -> {worker} alert"  #郵件標題
    content["from"] = sender  #寄件者
    content.attach(MIMEText(f"{worker} hashrate error.\nPlease check : {url}"))

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(sender, password)  # 登入寄件者gmail
            smtp.sendmail(sender, recipients, content.as_string())
            print("Alert Complete!")

        except Exception as e:
            print("Error message: ", e)
