from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .models import Advertising, Message
from .choices import MessageTypeChoices



@receiver(post_save, sender=Advertising)
def update_message_launch_time(sender, instance, **kwargs):
    if instance.launch_time and instance.top_time:
        start_time = instance.launch_time
        end_time = start_time + timedelta(hours=instance.top_time)

        conflicting_messages = Message.objects.filter(message_type=MessageTypeChoices.REGULAR,
            launch_time__gte=start_time,
            launch_time__lte=end_time,)

        if conflicting_messages:
            increment = timedelta(minutes=29)

            for message in conflicting_messages:
                message.launch_time = end_time
                message.save()
                end_time += increment

        else:
            print("No messages to move")


# @receiver(post_save, sender=Advertising)
# def upload_adv_to_excel(sender, instance, **kwargs):
#     if instance.launch_time:
#         now = timezone.now()
#
#         start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#         end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(microseconds=1)
#
#         messages_this_month = Message.objects.filter(launch_time__gte=start_of_month, launch_time__lte=end_of_month)
#
#         formatted_messages = "\n".join([f"{message.launch_time}" for message in messages_this_month])
# 
#         # Send messages to Telegram
#         send_messages_to_telegram_bot(formatted_messages)
#
#
#
# def send_messages_to_telegram_bot(messages):
#     token = settings.TELEGRAM_TOKEN
#
#     url = f"https://api.telegram.org/bot{token}/sendMessage"
#     data = {
#         'chat_id': "@blue_editor_bot",
#         'text': messages
#     }
#     response = requests.post(url, data=data)
#     if response.status_code != 200:
#         raise Exception(f"Error sending message: {response.text}")


