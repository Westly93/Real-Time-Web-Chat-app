# Generated by Django 3.1.4 on 2021-09-21 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='chatroom',
            new_name='chat_room',
        ),
    ]