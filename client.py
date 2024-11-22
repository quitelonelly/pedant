import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Авторизация с использованием учетных данных
gc = gspread.service_account(filename='/home/klim-petrov/projects/pedant_hakaton/creds.json')

# Открываем таблицу
ws = gc.open('Копия Сбор анкет').sheet1

# Получаем все данные
data = ws.get_all_records()

# Преобразуем данные в JSON
json_data = json.dumps(data, ensure_ascii=False, indent=4)  # Используем indent для красивого форматирования

# Определяем путь к файлу в корневой папке проекта
output_file_path = os.path.join(os.path.dirname(__file__), 'result.json')

# Сохраняем JSON в файл
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# Выводим сообщение о завершении
print(f"Данные успешно сохранены в {output_file_path}")