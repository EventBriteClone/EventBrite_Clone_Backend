# Generated by Django 4.2b1 on 2023-04-25 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0060_remove_event_images_myimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyImage',
        ),
    ]
