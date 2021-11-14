from collections import defaultdict
from django import forms
from datetime import date
from django.forms.widgets import NumberInput

HAS_DIGITAL= [
    ("True", "True"),
    ("False", "False"),
    ("Both", "Both")
]

class ManageBook(forms.Form):
    isbn = forms.CharField(max_length=13, required=True)
    book_name = forms.CharField(max_length=255, required=False)
    buy_price = forms.IntegerField(required=False)
    rent_price = forms.IntegerField(required=False)
    has_digital = forms.BooleanField(required=False)

class QueryBook (forms.Form):
    isbn = forms.CharField(max_length=13, required=False)
    book_name = forms.CharField(max_length=255, required=False)
    has_digital= forms.CharField(required=True, label='Has digital version or not?', widget=forms.Select(choices=HAS_DIGITAL))
