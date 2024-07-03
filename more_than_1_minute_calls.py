import json

# Функция для проверки времени в формате HH:MM:SS или MM:SS
def billing_time_greater_than_one_minute(billing_time):
    parts = billing_time.split(':')
    if len(parts) == 2:  # Формат MM:SS
        minutes = int(parts[0])
        seconds = int(parts[1])
    elif len(parts) == 3:  # Формат HH:MM:SS
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        minutes += hours * 60
    else:
        return False
    return minutes > 1 or (minutes == 1 and seconds > 0)

# Загрузка данных из файла
with open('json/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

keys_with_long_billing_time = []

# Обработка данных
for entry in data:
    key = entry.get('key')
    communication = entry.get('communication', [])
    for comm in communication:
        billing_time = comm.get('billing_time', '')
        if billing_time_greater_than_one_minute(billing_time):
            keys_with_long_billing_time.append(key)
            break  # Прекращаем проверку других вызовов для этого ключа

# Сохранение результатов в файл
with open('json/keys.json', 'w', encoding='utf-8') as outfile:
    json.dump(keys_with_long_billing_time, outfile, ensure_ascii=False, indent=4)

print("Результаты сохранены в файл 'keys.json'.")
