# Импортируем необходимые модули
import gspread
import json
import time

from message import send_email

# Задайте учетные данные
gc = gspread.service_account(filename='/home/klim-petrov/projects/pedant_hakaton/creds.json')
ws = gc.open('Копия Сбор анкет').sheet1
cities_ws = gc.open('Копия Сбор анкет').worksheet('список почт.с городами')

def append_to_google_sheet(data):

    # Открываем таблицу по ее имени
    gc = gspread.service_account(filename='/home/klim-petrov/projects/pedant_hakaton/creds.json')
    ws = gc.open('Копия Сбор анкет').sheet1  # Замените на ваше имя таблицы


    # Добавляем данные в таблицу

    ws.append_row(data)

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
                email = 'testlolohka@gmail.com' # Получаем почту для этого города
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