import requests
import json
import os

def send_telegram_message(chat_id, message_text, method, file_path=None):

    token = '5463745047:AAFf0BgFRYCFIrIEsRhXWZnDTucBbI2VEPs'  # hardcoded token

    url = f'https://api.telegram.org/bot{token}/{method}'  # hardcoded URL

    if method == 'sendPhoto' or method == 'sendVideo' and file_path:
        payload = {
            "chat_id": chat_id,
            "caption": message_text,
            "parse_mode": "MarkdownV2"
        }

        files = {
            'photo' if method == 'sendPhoto' else 'video': open(file_path, 'rb')
        }
        try:
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()  # Raise an error for bad status codes
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
                    'caption': message_text if i == 0 else ''  # Caption only for the first media item
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
            "parse_mode": "MarkdownV2"
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            print("Telegram message sent successfully.")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            return False

