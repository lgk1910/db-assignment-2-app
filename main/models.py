from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import CharField, NullBooleanField
from django.db.models.fields.related import ForeignKey
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    book_name = models.CharField(max_length=255)
    buy_price = models.IntegerField()
    rent_price = models.IntegerField()
    has_digital = models.BooleanField()

    def __str__(self):
        return f"{self.book_name} ({self.isbn})"
