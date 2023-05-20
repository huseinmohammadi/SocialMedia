# Generated by Django 4.2.1 on 2023-05-16 05:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_alter_message_chats_group_message_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='group_users', to=settings.AUTH_USER_MODEL),
        ),
    ]