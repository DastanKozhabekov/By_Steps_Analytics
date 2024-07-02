import json
import pandas as pd

# Загрузка исходного JSON файла
with open('json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Функция для преобразования данных в DataFrame
def transform_data_to_dataframe(data):
    rows = []
    for entry in data:
        segment_title = entry.get('segment_title')
        key = entry.get('key')
        if segment_title and key:
            communication = entry.get('communication', [])
            for i, com in enumerate(communication, start=1):
                step_name = f"Step {i}"
                status = com.get("status")
                rows.append({
                    'Segment Title': segment_title,
                    'Key': key,
                    'Step': step_name,
                    'Status': status
                })
    return pd.DataFrame(rows)

# Преобразование данных в DataFrame
df = transform_data_to_dataframe(data)

# Сохранение данных в Excel
excel_filename = 'excel/output_segment_title.xlsx'
df.to_excel(excel_filename, index=False)

print(f"Transformation complete. Check '{excel_filename}' for results.")
