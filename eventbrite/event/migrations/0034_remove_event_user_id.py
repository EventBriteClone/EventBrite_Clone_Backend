# Generated by Django 4.2b1 on 2023-04-13 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0033_event_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='User_id',
        ),
    ]
