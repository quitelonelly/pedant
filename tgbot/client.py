import gspread
from message import send_email

# Задайте учетные данные
gc = gspread.service_account(filename='/home/klim-petrov/projects/pedant_hakaton/creds.json')
ws = gc.open('Копия Сбор анкет').sheet1
cities_ws = gc.open('Копия Сбор анкет').worksheet('Копия список почт с городами')

# Запись данных в Google таблицу
def append_to_google_sheet(data):
    ws.append_row(data)

def get_last_record():
    data = ws.get_all_records()
    if data:
        last_record = data[-1]  # Получаем последнюю запись
        return last_record
    return None

# Получение списка городов и почт
def get_cities_list():
    cities_data = cities_ws.get_all_records()
    print("Данные из Google Sheets:", cities_data)  # Отладочное сообщение
    cities = {
        record['Город']: record['Список почт по городам']  # Используем правильные названия столбцов
        for record in cities_data 
        if 'Город' in record and 'Список почт по городам' in record and record['Город'] and record['Список почт по городам']
    }
    print("Список городов и почт:", cities)  # Отладочное сообщение
    return cities

# Проверка наличия города в списке
def check_city_in_list(city, cities):
    return city in cities

# Получение почты по городу
def get_email_by_city(city, cities):
    email = cities.get(city)
    print(f"По городу '{city}' найдена почта: {email}")  # Отладочное сообщение
    return email