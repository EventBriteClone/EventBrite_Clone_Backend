# Generated by Django 4.2b1 on 2023-04-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0036_event_summery'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(default='path', upload_to='event_images/'),
            preserve_default=False,
        ),
    ]