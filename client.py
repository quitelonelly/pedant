import gspread
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.service_account import Credentials
import json
import time

# Задайте учетные данные
gc = gspread.service_account(filename='C:\\Users\\хакатон\\creds.json')
ws = gc.open('Копия Сбор анкет').sheet1
cities_ws = gc.open('Копия Сбор анкет').worksheet('список почт.с городами')

# Укажите основные настройки для отправки электронной почты
SMTP_SERVER = 'smtp.gmail.com'  # Пример smtp-сервера
SMTP_PORT = 587  # Стандартный порт для TLS
SENDER_EMAIL = 'klimpetrov25@gmail.com'  # Ваш адрес электронной почты
SENDER_PASSWORD = 'sajb yozi okav utue'  # Ваш пароль

def get_last_record():
    data = ws.get_all_records()
    if data:
        last_record = data[-1]  # Получаем последнюю запись
        return last_record
    return None

def get_cities_list():
    cities_data = cities_ws.get_all_records()
    cities = {record['Город']: record['Список почт по городам'] for record in cities_data if 'Город' in record and 'Список почт по городам' in record}
    return cities

def check_city_in_list(city, cities):
    return city in cities

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Начинаем TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Авторизация
        server.send_message(msg)  # Отправка
        print(f'Письмо отправлено на {to_email}')
    except Exception as e:
        print(f'Не удалось отправить письмо: {e}')
    finally:
        server.quit()  # Закрываем соединение

def main():
    last_displayed_record = None
    cities = get_cities_list()  # Загружаем список городов и почт один раз

    while True:
        last_record = get_last_record()

        if last_record != last_displayed_record:
            last_displayed_record = last_record
            print("Последняя запись:", last_record)

            city = last_record.get('Город')  # Извлекаем город из последней записи
            if city and check_city_in_list(city, cities):
                email = cities[city]  # Получаем почту для этого города
                print(f"Город '{city}' найден в списке с почтой: {email}")

                # Отправляем электронное письмо
                subject = 'Информация о последней записи'
                body = json.dumps(last_record, ensure_ascii=False, indent=4)
                send_email(email, subject, body)
            else:
                print(f"Город '{city}' не найден в списке.")

        time.sleep(5)  # Задержка 5 секунд перед следующим запросом

if __name__ == "__main__":
    main()
