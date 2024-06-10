# Generated by Django 5.0.6 on 2024-06-06 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('launch_time', models.DateTimeField(blank=True, null=True)),
                ('message_text', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('WAITING', 'В ожидании'), ('SUCCESSFUL', 'Успешно'), ('FAILED', 'Провалено'), ('DELETED', 'Удаленно')], default='WAITING', max_length=100, null=True)),
                ('message_type', models.CharField(choices=[('REGULAR', 'Стандарт'), ('ADS', 'Реклама'), ('MARKED', 'Маркер')], max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TgChannel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('channel_id', models.CharField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publication.message')),
                ('belongs_to', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.CharField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, max_length=300, null=True)),
                ('top_time', models.IntegerField(blank=True, null=True)),
                ('delete_timer', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('publication.message',),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='message_img/')),
                ('video', models.FileField(upload_to='message_vid/')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publication.message')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='message',
            name='tg_channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publication.tgchannel'),
        ),
    ]