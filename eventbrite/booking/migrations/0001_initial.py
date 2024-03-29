# Generated by Django 4.2b1 on 2023-05-04 18:16

import booking.models
from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField(default=event.models.generate_unique_id, unique=True)),
                ('EVENT_ID', models.IntegerField(default=11111)),
                ('percent_off', models.IntegerField()),
                ('CODE', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('Quantity_available', models.IntegerField()),
                ('User_ID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField(default=booking.models.generate_unique_order_id, unique=True)),
                ('user_id', models.IntegerField(null=True)),
                ('event_id', models.IntegerField(null=True)),
                ('discount_id', models.IntegerField(null=True)),
                ('full_price', models.FloatField(null=True)),
                ('amount_off', models.FloatField(null=True)),
                ('fee', models.FloatField(null=True)),
                ('total', models.FloatField(null=True)),
                ('is_validated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField(default=booking.models.generate_unique_orderitem_id, unique=True)),
                ('order_id', models.IntegerField(null=True)),
                ('ticket_class_id', models.IntegerField(null=True)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('ticket_price', models.FloatField(null=True)),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('user_id', models.IntegerField(null=True)),
                ('event_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TicketClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField(default=booking.models.generate_unique_ticket_class_id, unique=True)),
                ('event_id', models.IntegerField()),
                ('User_id', models.IntegerField(blank=True, null=True)),
                ('NAME', models.CharField(blank=True, max_length=20, null=True)),
                ('PRICE', models.FloatField()),
                ('capacity', models.IntegerField()),
                ('quantity_sold', models.IntegerField()),
                ('TICKET_TYPE', models.CharField(blank=True, choices=[('Free', 'Free'), ('Paid', 'Paid'), ('Donation', 'Donation')], max_length=10, null=True)),
                ('Sales_start', models.DateField()),
                ('Sales_end', models.DateField()),
                ('Start_time', models.DateTimeField()),
                ('End_time', models.DateTimeField()),
                ('Absorb_fees', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=5)),
            ],
        ),
    ]
