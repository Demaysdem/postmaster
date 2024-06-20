from django.http import JsonResponse
from django.views import View
from .functions import send_telegram_message


class SendMessageView(View):
    def get(self, request):
        token = '5463745047:AAFf0BgFRYCFIrIEsRhXWZnDTucBbI2VEPs'  # Store your token in Django settings
        channel_username = '@test_23q21424'  # Store your channel username in settings
        message = "Hello, this is a message from my Django app!"

        response = send_telegram_message(token, channel_username, message)

        return JsonResponse(response)