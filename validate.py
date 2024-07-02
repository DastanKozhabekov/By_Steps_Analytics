import json

# Загрузка исходного JSON файла
with open('json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Функция для преобразования данных
def transform_data(data):
    result = {}
    for entry in data:
        segment_title = entry.get('segment_title')
        key = entry.get('key')
        if segment_title and key:
            communication = entry.get('communication', [])
            steps = {}
            for i, com in enumerate(communication, start=1):
                steps[f"Step {i}"] = {
                    "status": com.get("status")
                }
            if segment_title not in result:
                result[segment_title] = {}
            result[segment_title][key] = steps
    return result

# Преобразование данных
transformed_data = transform_data(data)

# Генерация JSON вручную
json_string = "{\n"
for segment, keys in transformed_data.items():
    json_string += f'    "{segment}": {{\n'
    for key, steps in keys.items():
        json_string += f'        "{key}": {{\n'
        for step, details in steps.items():
            json_string += f'            "{step}": {json.dumps(details)},\n'
        json_string = json_string.rstrip(',\n') + "\n"  # Удаляем последнюю запятую и перевод строки
        json_string += "        },\n"
    json_string = json_string.rstrip(',\n') + "\n"  # Удаляем последнюю запятую и перевод строки
    json_string += "    },\n"
json_string = json_string.rstrip(',\n') + "\n"  # Удаляем последнюю запятую и перевод строки
json_string += "}\n"

# Сохранение результатов в новый JSON файл
with open('json/output_segmentitle.json', 'w+', encoding='utf-8') as f:
    f.write(json_string)

print("Transformation complete. Check 'output.json' for results.")
