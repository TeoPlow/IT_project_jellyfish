import requests
import json
from IPython.display import display, Markdown

file_path = "C:\\Programs\\GitHub_Repositories\\IT_project_jellyfish\\DataSets\\По щучьему веленью.txt"
character_a = "Баба-Яга"
character_b = "Лёва"
token = "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.Np0rNwWMIwRPdNtoMKikeisxk_X8eEWui_KQtK0nvHzth2sDBROtcBkleNgP3AYW88maG1Oemhh7ebreFs5a2cnfl89LnLgAWxWDQDvmzDeZ-eb3fDyiNftwhiCQG2Ey5pUlDkLOMZYbgOYAjwEOaiSOa8YY-z8aaBTaHnx3TkDoZZuoXSVNemOA0gTh9-mMW32gyvrd5gGyDYC4N_ZNybaQPM_yC8F9Pq84UAEYPZ5SxbybHBTd9TUlZe2aYFSXBEkB5io3JsSyOXr2qRmnn2ZFr-LTJ6ncrk5nSxD65oNxpuhsBett-44SvPOd00zz5rZ5d5kDLLNoM8YlddzJwA.AYgVV0MX-Nz100oJZtcBMA.IQbXvybBwGuAh_X-YrSEs9zbNnqBTqDUAw5vuktRSVlUTY3CPreInmXMMwRsc753X-zfuln0Xn7xHlZs3UB4EwXdOHxirPb7SUulzCfU51zbuYqespyfebg7N_qpSrZ9dQ2VPgW0-36H6AOxmYdUyRLG3yzsvtxNgw7OXI_UcLkMu0lQBUcFD-yEZAZq0VNLbC-cMSTLD_Tw7ry1NwXNf5pK4WqcQ9ORPGC8w1CNoE5Yup05ufmLIsaxlpiHn1M95yxHymsqoLY3D94rb138qxiw8ugRypsI1cdMvnvaQsPk5ipx5EVqOQbVG65RK9S4srOS0OO0qIOKLe4uJ-xS6hu20DgRfd6wGJOi8UM-SAH3aW2_-L5YgiUh33j1Vc2hUFeWNqTMDAbx4epfiFkyr4JlPde1Si4ztdxUR3a5WzPqeKXW11zWpMyERornmYzILNo7z8T7q_LWQImqdlfyWd8e2eJAe_W2WgOwa1KPQyNlpZruISxweW6t-Wr3iQJLky1GQA0bHgGI8HRStjlpJKXkUGhGWQnju4FWwoLIkOgZfGuxONgOTWEgOPGB3daT-4TSopKL5OIxfGRHiZ4nGlB_8otZxGvWk0VIf85F8h4Io0jvzlXU-CfkWXJdLxRQ-nOJtSn5kXcg34Tm_Uyjtyjz3_3BgutyEl5kPpLPjZ33dvIkmcJepCEEzK70_h_tGkz91qZZwpTPD6Xr9-HO8YG9JtaHrSCSbURAoPfnDEA.eeYjnnsvsARzFmXpQGJjjbSWnh1ouZBL81HJl6v1uK8"
cluster_length = 4000

def get_chat_completion(auth_token, user_message):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.

    Возвращает:
    - str: Ответ от API в виде текстовой строки.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 2,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 4000,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 1  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1

def replace_characters(file_path, character_a, character_b):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Вычисляем длину строки и вычитаем её из cluster_length
        max_cluster_length = cluster_length - len(f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n")

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

results = replace_characters(file_path, character_a, character_b)
for result in results:
    giga_token = token
    answer = get_chat_completion(giga_token, result)
     
    answer.json()

    print(answer.json()['choices'][0]['message']['content'])
     
    display(Markdown(answer.json()['choices'][0]['message']['content']))

# def print_to_txt ():
#     # создаёте функцию для вывода текста в файл
