from celery import shared_task
from post_master.celery import app
from .models import Message, Advertising, Image, Video
from .choices import MessageStatusChoices, MessageTypeChoices
from datetime import datetime, timedelta
from .functions import send_telegram_message, delete_message


@app.task
def check_message_status():
    print("hello")
    one_minute_ago = datetime.now() - timedelta(minutes=1)

    advertisements_to_delete = Advertising.objects.filter(status=MessageStatusChoices.SUCCESSFUL,
                               message_type=MessageTypeChoices.ADS,
                               delete_timer__gte=one_minute_ago,
                               delete_timer__lte=datetime.now())

    messages = Message.objects.filter(status=MessageStatusChoices.WAITING, launch_time__gte=one_minute_ago,
                                  launch_time__lte=datetime.now())

    if messages:
        print('Messages preparing to send')
        perform_sending_messages(messages)
    else:
        print('Nothing to send')

    if advertisements_to_delete:
        print('Preparing to delete advertisement')
        perform_deleting_advertisement(advertisements_to_delete)
    else:
        print('Nothing to delete')



@shared_task
def perform_sending_messages(messages):
    for message in messages:
        tg_channel = message.tg_channel
        chat_id = tg_channel.channel_id
        message_text = message.message_text

        images = Image.objects.filter(message_id=message.id)
        videos = Video.objects.filter(message_id=message.id)

        img_count = len(images)
        vid_count = len(videos)

        if images or videos:
            if img_count == 1 and vid_count == 0:
                single_image = images.first()
                method = 'sendPhoto'
                file_path = single_image.image.path

                success = send_telegram_message(chat_id, message, message_text, method, file_path)

            elif img_count == 0 and vid_count == 1:
                single_video = videos.first()
                method = 'sendVideo'
                file_path = single_video.video.path

                success = send_telegram_message(chat_id, message, message_text, method, file_path)

            elif 2 <= img_count + vid_count <= 10:
                method = 'sendMediaGroup'
                image_paths = [img.image.path for img in images]
                video_paths = [vid.video.path for vid in videos]
                file_paths = image_paths + video_paths

                success = send_telegram_message(chat_id, message, message_text, method, file_paths)

            else:
                print('Too much media files')

        else:
            method = 'sendMessage'
            success = send_telegram_message(chat_id, message, message_text, method, None)

        if success:
            print('Message sent successfully')
            message.message_item(MessageStatusChoices.SUCCESSFUL,)

        else:
            print('Send error')
            message.message_item(MessageStatusChoices.FAILED,)


@shared_task
def perform_deleting_advertisement(advertisements_to_delete):
    for adv_to_del in advertisements_to_delete:
        method = 'deleteMessage'
        tg_channel = adv_to_del.tg_channel
        chat_id = tg_channel.channel_id
        message_id = adv_to_del.tg_message_id
        success = delete_message(chat_id, method, message_id)
        if success:
            adv_to_del.message_item(MessageStatusChoices.DELETED,)
        else:
            print('Delete error')
