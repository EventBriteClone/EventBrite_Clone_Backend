# Generated by Django 4.2b1 on 2023-04-17 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0046_event_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ID',
            field=models.IntegerField(),
        ),
    ]