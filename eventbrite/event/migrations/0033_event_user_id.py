# Generated by Django 4.2b1 on 2023-04-13 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0032_remove_userinterest_sub_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='User_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
