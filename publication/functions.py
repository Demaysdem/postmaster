import requests
import json
import os
from django.conf import settings


def send_telegram_message(chat_id,message, message_text, method, file_path=None):

    token = settings.TELEGRAM_TOKEN

    url = f'https://api.telegram.org/bot{token}/{method}'  # hardcoded URL

    if method == 'sendPhoto' or method == 'sendVideo' and file_path:
        payload = {
            "chat_id": chat_id,
            "caption": message_text,
            "parse_mode": "HTML"
        }

        files = {
            'photo' if method == 'sendPhoto' else 'video': open(file_path, 'rb')
        }
        try:
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
            response_json = response.json()
            message.tg_message_id_item(response_json['result']['message_id'])
            print("Telegram message sent successfully.")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            return False


    elif method == 'sendMediaGroup' and file_path:
        media = []
        files = {}
        for i, file_path in enumerate(file_path):
            if os.path.isfile(file_path):
                file_type = 'photo' if file_path.lower().endswith(('jpg', 'jpeg', 'png')) else 'video'
                media.append({
                    'type': file_type,
                    'media': f'attach://file{i}',
                    'caption': message_text if i == 0 else ''
                })
                files[f'file{i}'] = open(file_path, 'rb')
            else:
                print(f"Skipping invalid file path: {file_path}")

        payload = {
            "chat_id": chat_id,
            "media": json.dumps(media),
        }

        try:
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
            response_json = response.json()
            message.tg_message_id_item(response_json['result']['message_id'])
            print("Telegram media group sent successfully.")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram media group: {e}")
            return False

        except IOError as e:
            print(f"Error opening file: {e}")
            return False

        finally:
            if files:
                for file in files.values():
                    file.close()

    else:

        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            response_json = response.json()
            message.tg_message_id_item(response_json['result']['message_id'])
            print("Telegram message sent successfully.")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            return False


def delete_message(chat_id, method, message_id):
    token = settings.TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{token}/{method}"
    params = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    try:
        response = requests.get(url, params=params)
        print(f"Message {message_id} in chat {chat_id} deleted successfully")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to delete message {message_id} in chat {chat_id}:{e}")
        return False