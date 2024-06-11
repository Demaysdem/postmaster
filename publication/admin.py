from django.contrib import admin
from .models import TgChannel, Message, Advertising, Image, Video
from django.contrib.admin.options import TabularInline


class ImageAdminInline(TabularInline):
        extra = 1
        model = Image


class VideoAdminInline(TabularInline):
        extra = 1
        model = Video


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Video)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(TgChannel)
class TgChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'channel_id',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'launch_time', 'status', 'message_type')
    inlines = (ImageAdminInline,VideoAdminInline)


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'launch_time', 'message_type', 'status', 'belongs_to', 'price', 'comment', 'top_time')
    inlines = (ImageAdminInline,VideoAdminInline)
