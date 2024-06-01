from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import os
import requests
import json
import uuid
import re
import threading

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'uploads'
application.config['DOWNLOAD_FOLDER'] = 'downloads'

# Глобальный флаг для отслеживания состояния обработки
processing_lock = threading.Lock()

# Функция для получения токена авторизации
def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }
    payload = {'scope': scope}

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

# Получение токена авторизации
auth_token = "NzQ3YjhiNzctNjYxZC00YmRkLWIyYmUtOGViMDZjMzZiYWRmOjkzY2UzYWJhLTFmMjktNDc4My1iYzIyLWQzMjgzODI2MGExMw=="
response = get_token(auth_token)
if response != -1:
    token = response.json()['access_token']

# Функция для отправки запроса к нейросети и получения результата
def get_chat_completion(auth_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 4000,
        "repetition_penalty": 1,
        "update_interval": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return -1

# Функция для обработки файла и отправки запроса к нейросети
def process_file(text_file, character_a, character_b):
    if not os.path.exists(application.config['UPLOAD_FOLDER']):
        os.makedirs(application.config['UPLOAD_FOLDER'])

    text_file_path = os.path.join(application.config['UPLOAD_FOLDER'], text_file.filename)
    text_file.save(text_file_path)

    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        max_cluster_length = 4000 - len(f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n")
        clusters = []
        cluster_number = 1

        while len(text) > 0:
            if len(text) <= max_cluster_length:
                cluster_text = text[:max_cluster_length]
                text = text[max_cluster_length:]
            else:
                last_period_index = text[:max_cluster_length].rfind('.')
                cluster_text = text[:last_period_index + 1]
                text = text[last_period_index + 1:]

            cluster = f"Кластер {cluster_number}:\n"
            cluster += f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n"
            cluster += cluster_text + '\n'
            clusters.append(cluster)
            cluster_number += 1

        return clusters

    except FileNotFoundError:
        return ["Указанный файл не найден."]

@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if processing_lock.locked():
            return jsonify({"status": "error", "message": "Запрос уже обрабатывается. Пожалуйста, подождите."})

        processing_lock.acquire()
        try:
            text_file = request.files["text_file"]
            character_a = request.form["character_a"]
            character_b = request.form["character_b"]

            edited_text = process_file(text_file, character_a, character_b)

            if isinstance(edited_text, str):
                return edited_text
            else:
                output_text = ""
                for cluster in edited_text:
                    answer = get_chat_completion(token, cluster)
                    if answer == -1:
                        return jsonify({"status": "error", "message": "Ошибка при обработке запроса к нейросети."})
                    output_text += answer.json()['choices'][0]['message']['content']

                if not os.path.exists(application.config['DOWNLOAD_FOLDER']):
                    os.makedirs(application.config['DOWNLOAD_FOLDER'])

                output_file_path = os.path.join(application.config['DOWNLOAD_FOLDER'], "edited_text.txt")
                with open(output_file_path, "w", encoding="utf-8") as f:
                    # Фильтруем вывод программы
                    output_text = re.sub(r'Кластер \d+:', '', output_text)

                    # Удаляем лишние пробелы в начале и конце строки
                    output_text = output_text.strip()
                    f.write(output_text)

                return jsonify({"status": "success", "message": "Файл успешно обработан. Начинаю загрузку."})
        finally:
            processing_lock.release()

    return render_template("index.html")

@application.route("/download")
def download_file():
    output_file_path = os.path.join(application.config['DOWNLOAD_FOLDER'], "edited_text.txt")
    return send_file(output_file_path, as_attachment=True)

if __name__ == "__main__":
    application.run()
