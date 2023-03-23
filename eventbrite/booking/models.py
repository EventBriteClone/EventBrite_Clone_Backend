from django.db import models

# Create your models here.
class Ticket(models.Model):
    ID=models.IntegerField()
    NAME=models.CharField(max_length=20)
    PRICE=models.FloatField()
    EVENT_ID=models.IntegerField()
    GUEST_ID=models.IntegerField()
    TICKET_NUM=models.IntegerField()
    TICKET_TYPE=models.Choices("Free","VIP")


class Discount(models.Model):
  ID=models.IntegerField()
  EVENT_ID=list()
  percent_off =models.CharField(max_length=20)
  CODE=models.CharField(max_length=20)
  start_date=models.DateField()
  end_date=models.DateField()
  Quantity_available =models.IntegerField()
  User_ID=models.IntegerField()