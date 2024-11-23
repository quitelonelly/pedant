# Импортируем необходимые модули
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv # type: ignore

# Основные настройки для отправки электронной почты
SMTP_SERVER = 'smtp.gmail.com'  # Адрес SMTP-сервера
SMTP_PORT = 587 # Порт для TLS

# Функция для отправки электронного письма
def send_email(to_email, subject, body):
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    sender_pass = os.getenv("SENDER_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Начинаем TLS
        server.login(sender_email, sender_pass)  # Авторизация
        server.send_message(msg)  # Отправка
        print(f'Письмо отправлено на {to_email}')
    except Exception as e:
        print(f'Не удалось отправить письмо: {e}')
    finally:
        server.quit()  # Закрываем соединение