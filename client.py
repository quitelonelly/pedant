import gspread
from google.oauth2.service_account import Credentials
import json

# Авторизация с использованием учетных данных
gc = gspread.service_account(filename='/home/klim-petrov/projects/pedant_hakaton/creds.json')

# Открываем таблицу
ws = gc.open('Копия Сбор анкет').sheet1

# Получаем все данные
data = ws.get_all_records()

# Преобразуем данные в JSON
json_data = json.dumps(data, ensure_ascii=False, indent=4)  # Используем indent для красивого форматирования

# Сохраняем JSON в файл
with open('result.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# Выводим сообщение о завершении
print("Данные успешно сохранены в result.json")