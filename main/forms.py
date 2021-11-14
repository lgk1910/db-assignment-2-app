from collections import defaultdict
from django import forms
from datetime import date
from django.forms.widgets import NumberInput

HAS_DIGITAL= [
    ("True", "True"),
    ("False", "False"),
    ("Both", "Both")
]

SORT_OPT = [
    ("not_sort", "Not sort"),
    ("book_name", "Title"),
    ("buy_price", "Buy price"),
    ("rent_price", "Rent price"),
]

ORDER = [
    ("asc", "Ascending"),
    ("desc", "Descending")
]

class ManageBook(forms.Form):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')
    book_name = forms.CharField(max_length=255, required=False)
    buy_price = forms.IntegerField(required=False)
    rent_price = forms.IntegerField(required=False)
    has_digital = forms.BooleanField(required=False)

class QueryBook (forms.Form):
    isbn = forms.CharField(max_length=13, required=False, label='ISBN')
    book_name = forms.CharField(max_length=255, required=False)
    has_digital= forms.CharField(required=True, label='Has digital version or not?', widget=forms.Select(choices=HAS_DIGITAL))
    sort = forms.CharField(required=True, label='Sort or not?', widget=forms.Select(choices=SORT_OPT))
    order = forms.CharField(required=True, label='Ascending or Descending?', widget=forms.Select(choices=ORDER))
