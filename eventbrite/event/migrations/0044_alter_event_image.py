# Generated by Django 4.2b1 on 2023-04-15 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0043_category_locations_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to='events/'),
        ),
    ]
