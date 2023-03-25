# Generated by Django 4.2b1 on 2023-03-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_rename_descriiption_event_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='Name',
            new_name='Title',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='TYPE',
            new_name='type',
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.CharField(default='string', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='sub_Category',
            field=models.CharField(default='string', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='venue_name',
            field=models.CharField(default='string', max_length=20),
            preserve_default=False,
        ),
    ]
