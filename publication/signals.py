from django.db.models.signals import post_save, pre_save
from django.db.models import Q
from django.core.exceptions import ValidationError


from django.dispatch import receiver
from django.utils.timezone import now
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
            print("No messages to move ")


# validation to do
# 1. If user trying to create message with launching time overlaping advertisment top time need to throw the error
# only if both of them have same tg_channel
#
# 2. If user trying to create advertisment with launching time overlaping advertisment top time need to throw the error
# only if both of them have same tg_channel






