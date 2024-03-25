def replace_characters(file_path, character_a, character_b):
    try:
        # Открываем файл и считываем его содержимое
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Разбиваем текст на кластеры
        clusters = []
        cluster_number = 1
        while len(text) > 0:
            if len(text) <= 4000:
                cluster_text = text[:4000]
                text = text[4000:]
            else:
                last_period_index = text[:4000].rfind('.')  # Находим последнюю точку перед 4000 символами
                cluster_text = text[:last_period_index+1]
                text = text[last_period_index+1:]

            cluster = f"Кластер {cluster_number}:\n"
            cluster += f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n"
            cluster += cluster_text + '\n'
            clusters.append(cluster)
            cluster_number += 1

        return clusters

    except FileNotFoundError:
        return ["Указанный файл не найден."]

# Запрос пути к файлу и данных для замены
request = r"D:\sisisi\text.txt A B"

# Разбиваем введенную строку на компоненты
file_path, character_a, character_b = map(str.strip, request.split())

# Применяем функцию замены и выводим результат
results = replace_characters(file_path, character_a, character_b)
for result in results:
    print(result)
