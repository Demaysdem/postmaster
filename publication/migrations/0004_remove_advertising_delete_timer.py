# Generated by Django 5.0.6 on 2024-06-11 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0003_image_video_delete_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertising',
            name='delete_timer',
        ),
    ]
