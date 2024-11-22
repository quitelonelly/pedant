import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Авторизация с использованием учетных данных
gc = gspread.service_account(filename='/home/klim-petrov/projects/pedant_hakaton/creds.json')

# Открываем листы
applications_ws = gc.open('Копия Сбор анкет').worksheet('Лист1')  # Лист с новыми заявками
cities_ws = gc.open('Копия Сбор анкет').worksheet('список почт.с городами')  # Лист со списком почт и городов
# функция для отображение последней записи
def get_last_record():
    data = ws.get_all_records()
    if data:
        last_record = data[-1]  # Получаем последнюю запись
        return json.dumps(last_record, ensure_ascii=False)
    return None

def main():
    last_displayed_record = None

    while True:
        last_record = get_last_record()
        
        if last_record != last_displayed_record:
            last_displayed_record = last_record
            print("Последняя запись:", last_record)

        time.sleep(5)  # Задержка 5 секунд перед следующим запросом

data = ws.get_all_records()

json_data = json.dumps(data, ensure_ascii=False, indent=4)  # Используем indent для красивого форматирования


# Получаем все данные из листа с заявками
applications_data = applications_ws.get_all_records()

# Получаем все города из листа со списком почт
cities_data = cities_ws.get_all_records()

# Извлекаем список городов
cities = {row['Город'] for row in cities_data}  # Предполагается, что в таблице есть столбец 'Город'

# Проверяем каждую заявку
for application in applications_data:
    city = application.get('Город')  # Предполагается, что в заявке есть столбец 'Город'
    
    if city in cities:
        print(f"Город '{city}' из заявки найден в списке городов.")
    else:
        print(f"Город '{city}' из заявки НЕ найден в списке городов.")

# Преобразуем данные в JSON
json_data = json.dumps(applications_data, ensure_ascii=False, indent=4)

# Определяем путь к файлу в корневой папке проекта
output_file_path = os.path.join(os.path.dirname(__file__), 'result.json')

# Сохраняем JSON в файл
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
# выводим последнюю запись    
if __name__ == "__main__":
    main()

# Выводим сообщение о завершении
print(f"Данные успешно сохранены в {output_file_path}")
