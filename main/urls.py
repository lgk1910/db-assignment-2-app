from django.urls import path, include

from main.forms import QueryBook
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('managebook/', views.manageBook, name='manage_book'),
    path('querybook/', views.queryBook, name='manage_book'),
]