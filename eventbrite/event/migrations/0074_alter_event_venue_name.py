# Generated by Django 4.2b1 on 2023-04-26 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0073_alter_event_venue_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue_name',
            field=models.CharField(default='True', max_length=20),
            preserve_default=False,
        ),
    ]
