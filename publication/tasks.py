from celery import shared_task
from post_master.celery import app

from .models import Message, Advertising, Image, Video
from .choices import MessageStatusChoices, MessageTypeChoices
from datetime import datetime, timedelta
from .functions import send_telegram_message


@app.task
def check_message_status():
    print("hello")
    one_minute_ago = datetime.now() - timedelta(minutes=1)

    advertisements_to_delete = Advertising.objects.filter(status=MessageStatusChoices.SUCCESSFUL,
                                                          message_type=MessageTypeChoices.ADS,
                                                delete_timer__lte=one_minute_ago)

    messages = Message.objects.filter(status=MessageStatusChoices.WAITING, launch_time__gte=one_minute_ago,
                                  launch_time__lte=datetime.now())

    if messages:
        print('Advertisements preparing to send')
        perform_sending_messages(messages)

    elif advertisements_to_delete:
        print('Preparing to delete advertisement')
        perform_deleting_advertisement(advertisements_to_delete)

    else:
        print('Nothing to delete or send')


@shared_task
def perform_sending_messages(messages):
    for message in messages:

        method = 'sendMessage'
        tg_channel = message.tg_channel
        chat_id = tg_channel.channel_id
        message_text = message.message_text

        images = Image.objects.filter(message=message)
        videos = Video.objects.filter(message=message)

        img_count = len(images)
        vid_count = len(videos)

        if images or videos:
            if img_count == 1 and vid_count == 0:
                single_image = images.first()
                method = 'sendPhoto'
                file_path = single_image.image.path
                success = send_telegram_message(chat_id, message, method, file_path)

            elif img_count == 0 and vid_count == 1:
                single_video = videos.first()
                method = 'sendVideo'
                file_path = single_video.video.path
                success = send_telegram_message(chat_id, message, method, file_path)

            else:
                image_paths = [img.image.path for img in images]
                video_paths = [vid.video.path for vid in videos]
                file_paths = image_paths + video_paths

                # Adjust the method name based on how you plan to send multiple files
                method = 'sendMediaGroup'
                success = send_telegram_message(chat_id, message_text, method, file_paths)

        else:
            method = 'sendMessage'
            success = send_telegram_message(chat_id, message_text, method, None)

        if success:
            print('Message sent successfully')
            message.message_item(MessageStatusChoices.SUCCESSFUL,)

        else:
            print('Send error')
            message.message_item(MessageStatusChoices.FAILED,)


@shared_task
def perform_deleting_advertisement(advertisements_to_delete):
    for adv_to_del in advertisements_to_delete:
        channel_id = adv_to_del.tgchannel_set.values_list('channel_id', flat=True)

# File Name: message_files/Снимок_экрана_2024-06-05_в_16.46.08_QfVRxkE.png
# File URL: /media/message_files/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-06-05_%D0%B2_16.46.08_QfVRxkE.png
# File Name: message_files/Снимок_экрана_2024-06-04_в_16.49.51_NDLAXXU.png
# File URL: /media/message_files/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-06-04_%D0%B2_16.49.51_NDLAXXU.png
