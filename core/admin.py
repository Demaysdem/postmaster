from django.contrib import admin
from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_type', 'object_id', 'action_time', 'object_repr', 'action_flag')
    list_filter = ('user',  'action_flag',)
    search_fields = ('action_time',)