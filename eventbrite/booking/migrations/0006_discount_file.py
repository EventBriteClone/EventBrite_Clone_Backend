# Generated by Django 4.2b1 on 2023-05-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_discount_ends_alter_discount_starts'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='file',
            field=models.FileField(default='file', upload_to='csv/'),
            preserve_default=False,
        ),
    ]
