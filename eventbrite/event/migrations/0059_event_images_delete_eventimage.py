# Generated by Django 4.2b1 on 2023-04-25 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0058_remove_event_image4_remove_event_image5_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='images',
            field=models.FileField(blank=True, null=True, upload_to='events/'),
        ),
        migrations.DeleteModel(
            name='EventImage',
        ),
    ]
