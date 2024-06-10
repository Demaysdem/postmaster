import requests


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
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "MarkdownV2"
        }
        print('hi')

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


# def send_telegram_single_media(chat_id, message, method, file_path):
#
#     token = '5463745047:AAFf0BgFRYCFIrIEsRhXWZnDTucBbI2VEPs'  # hardcode
#     url = f'https://api.telegram.org/bot{token}/{method}'  # hardcode
#
#     if method == 'sendPhoto':
#         payload = {
#             "photo": file_path,
#             "caption": message if message else None
#         }
#     else:
#         payload = {
#             "video": file_path,
#             "caption": message if message else None
#         }
#     try:
#         response = requests.post(url, json=payload)
#         print("Telegram file sent successfully.")
#         return True
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error sending Telegram message: {e}")


# def send_telegram_media_group(chat_id, message, method, media):
#
#     token = '5463745047:AAFf0BgFRYCFIrIEsRhXWZnDTucBbI2VEPs'  # hardcode
#     url = f'https://api.telegram.org/bot{token}/{method}'  # hardcode
#
#     media_group = []
#     return True


