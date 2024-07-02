import pandas as pd

# Загрузка данных из Excel
df = pd.read_excel('excel/output_segment_title.xlsx', sheet_name='Sheet1')

# Инициализация счетчиков
dozvon_counts = {f'Шаг {i + 1}': 0 for i in range(10)}  # Счетчики дозвонов по шагам (Шаг 1, Шаг 2, ..., Шаг 10)
avtootvet_counts = {f'Шаг {i + 1}': 0 for i in range(10)}  # Счетчики автоответчиков по шагам (Шаг 1, Шаг 2, ..., Шаг 10)
nedozvon_counts = 0  # Счетчик недозвонов

# Обработка данных
for index, row in df.iterrows():
    segment_title = row['Segment Title']
    key = row['Key']
    step = row['Step']
    status = row['Status']

    if 'Step' in step:
        step_number = int(step.split()[-1])  # Получаем номер шага из строки 'Step X'

        if 1 <= step_number <= 10:  # Учитываем только шаги от 1 до 10
            # Проверка на шаг и статус для дозвона
            if status == 'Answered':
                dozvon_counts[f'Шаг {step_number}'] += 1

            # Проверка на сегмент и статус для автоответчика
            if segment_title in ['Автоответчик', 'Автоответчик Доставлено', 'Не доставлено Автоответчик']:
                avtootvet_counts[f'Шаг {step_number}'] += 1

    # Проверка на сегмент для недозвона
    if segment_title in ['Недозвон Доставлено', 'Недозвон']:
        nedozvon_counts += 1
    # Проверка на статус для недозвона
    elif status in ['The client does not answer the call', 'No spare channels']:
        if 'Step' in step:
            step_number = int(step.split()[-1])
            if 1 <= step_number <= 10:
                nedozvon_counts += 1

# Формирование таблицы для вывода
results = pd.DataFrame(
    columns=['Дозвон', 'Автоответчики', 'Реальный дозвон', 'Общ. Заинтересованные', 'Заинтересованные',
             'Средне-заинтересованные'])

# Добавление строк для каждого шага и категории
for i in range(10):
    step = f'Шаг {i + 1}'
    dozvon = dozvon_counts[step]
    avtootvet = avtootvet_counts[step]
    real_dozvon = dozvon - avtootvet
    results.loc[step] = [dozvon, avtootvet, real_dozvon, 0, 0, 0]

# Добавление строки для недозвона
results.loc['Недозвон'] = [nedozvon_counts, 0, 0, 0, 0, 0]

# Сохранение результатов в файл Excel
results.to_excel('excel/BASA.xlsx', index=True)

print("Результаты сохранены в файл 'BASA.xlsx'.")
