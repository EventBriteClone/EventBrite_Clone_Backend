# Generated by Django 4.2b1 on 2023-03-24 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_event_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Discount',
        ),
        migrations.DeleteModel(
            name='Tickets',
        ),
    ]
