def replace_characters(file_path, character_a, character_b):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Вычисляем длину строки и вычитаем её из 4000
        max_cluster_length = 4000 - len(f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n")

        clusters = []
        cluster_number = 1
        while len(text) > 0:
            if len(text) <= max_cluster_length:
                cluster_text = text[:max_cluster_length]
                text = text[max_cluster_length:]
            else:
                last_period_index = text[:max_cluster_length].rfind('.')
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

request = r"D:\sisisi\text.txt A B"
file_path, character_a, character_b = map(str.strip, request.split())

results = replace_characters(file_path, character_a, character_b)
for result in results:
    print(result)
