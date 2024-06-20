from django.db import models
from .choices import MessageStatusChoices, MessageTypeChoices
from core.models import TimeStampMixin
from django.core.exceptions import ValidationError
from datetime import timedelta


class TgChannel(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    channel_id = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name


class Message(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    tg_message_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    launch_time = models.DateTimeField(null=True, blank=True)
    message_text = models.TextField(null=True, blank=True)
    tg_channel = models.ForeignKey(TgChannel, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default=MessageStatusChoices.WAITING, choices=MessageStatusChoices.choices, null=True, blank=True)
    message_type = models.CharField(max_length=100, choices=MessageTypeChoices.choices)

    def message_validation(self, *args, **kwargs):
        if self.launch_time:
            overlapping_ads = Advertising.objects.filter(message_type=MessageTypeChoices.ADS,
                tg_channel=self.tg_channel
            ).exclude(id=self.id)

            for ad in overlapping_ads:
                ad_end_time = ad.launch_time + timedelta(hours=ad.top_time)
                if ad.launch_time <= self.launch_time < ad_end_time:
                    return False
        return True

    def clean(self):
        if not self.message_validation():
            raise ValidationError({"launch_time": "Message launch time overlaps with an advertisement top time for the same channel."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def message_item(self, status):
        self.status = status
        self.save()

    def tg_message_id_item(self, tg_message_id):
        self.tg_message_id = tg_message_id
        self.save()


    def __str__(self):
        return str(self.name)


class Advertising(Message):
    belongs_to = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(null=True, blank=True)
    comment = models.TextField(max_length=300, null=True, blank=True)
    top_time = models.IntegerField(null=True, blank=True)
    delete_timer = models.DateTimeField(null=True, blank=True)

    def ads_validation(self, *args, **kwargs):
        if self.launch_time and self.top_time:
            overlapping_ads = Advertising.objects.filter(message_type=MessageTypeChoices.ADS,
                tg_channel=self.tg_channel
            ).exclude(id=self.id)

            for ad in overlapping_ads:
                print(ad)
                ad_end_time = ad.launch_time + timedelta(hours=ad.top_time)
                if not (self.launch_time >= ad_end_time or self.launch_time + timedelta(
                        hours=self.top_time) <= ad.launch_time):
                    return False
        return True

    def clean(self):
        if not self.ads_validation():
            raise ValidationError({"launch_time": "Advertising launch time overlaps with another advertisement top "
                                                  "time for the same channel."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Advertising: {self.name} - {self.status}"


class Image(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='message_img/', null=True, blank=True)
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.CASCADE)


class Video(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    video = models.FileField(upload_to='message_vid/', null=True, blank=True)
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.CASCADE)
