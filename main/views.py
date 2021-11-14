from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib import messages
import random

TF_MAPPING = {
    'True': 1,
    'False': 0,
    'Both': -1
}

# Create your views here.
def index(request, id):
    return render(request, "main/home.html", {})

def home(request):
    return render(request, "main/home.html", {})

def manageBook(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = ManageBook(request.POST)
            if request.POST.get("save"):
                if form.is_valid():
                    try:
                        Book.objects.create(isbn=form.cleaned_data["isbn"], 
                                            book_name=form.cleaned_data["book_name"], 
                                            buy_price=form.cleaned_data["buy_price"], 
                                            rent_price=form.cleaned_data["rent_price"],
                                            has_digital=form.cleaned_data["has_digital"])
                    except:  
                        messages.error(request, "Duplicated ISBN or missing value. Please check again!")
            elif request.POST.get("update"):
                if form.is_valid():
                    try:
                        updated_book = Book.objects.get(isbn=form.cleaned_data['isbn'])
                    except:
                        messages.error(request, "Book does not exist.")
                        form = ManageBook()
                        books = Book.objects.all()
                        return render(request, 'main/manageBook.html', context={'books': books, 'form': form})

                    if form.cleaned_data["book_name"]:
                        updated_book.book_name = form.cleaned_data["book_name"]
                    if form.cleaned_data["buy_price"]:
                        updated_book.buy_price = form.cleaned_data["buy_price"]
                    if form.cleaned_data["rent_price"]:
                        updated_book.rent_price = form.cleaned_data["rent_price"]
                    updated_book.save()

            elif request.POST.get("delete"):
                if form.is_valid():
                    Book.objects.get(isbn=form.cleaned_data["isbn"]).delete()
        form = ManageBook()
        books = Book.objects.all()
        return render(request, 'main/manageBook.html', context={'books': books, 'form': form})
    else:
        messages.error(request, "Only superuser is allowed to add new book. Please login into a superuser account.")
        return redirect('/login')

def queryBook(request):
    if request.method == "POST":
        form = QueryBook(request.POST)
        if form.is_valid():
            if form.cleaned_data['isbn']:
                try:
                    books = Book.objects.filter(isbn__contains=form.cleaned_data['isbn'])
                except:
                    return render(request, 'main/queryBook.html', context={'books': None, 'form': form})
            if form.cleaned_data['book_name']:
                try:
                    books = books.filter(book_name__contains=form.cleaned_data['book_name'])
                except:
                    try:
                        books = Book.objects.filter(book_name__contains=form.cleaned_data['book_name'])
                    except:
                        pass

            # Filter by has_digital
            if form.cleaned_data['has_digital']:
                has_digital = TF_MAPPING[form.cleaned_data['has_digital']]
                if has_digital != -1:
                    try:
                        books = books.filter(has_digital=has_digital)
                    except:
                        try:
                            books = Book.objects.filter(has_digital=has_digital)
                        except:
                            pass
                else:
                    books = Book.objects

            # Filter by buy price
            try:
                books = books.filter(buy_price__gte=int(request.POST.get('start_buy_price')), 
                                     buy_price__lte=int(request.POST.get('end_buy_price')))
            except:
                books = Book.objects.filter(buy_price__gte=int(request.POST.get('start_buy_price')), 
                                            buy_price__lte=int(request.POST.get('end_buy_price')))
                
            # Filter by rent price
            try:
                books = books.filter(rent_price__gte=int(request.POST.get('start_rent_price')), 
                                     rent_price__lte=int(request.POST.get('end_rent_price')))
            except:
                books = Book.objects.filter(rent_price__gte=int(request.POST.get('start_rent_price')), 
                                            rent_price__lte=int(request.POST.get('end_rent_price')))

            # Sorted or not 
            sort_opt = form.cleaned_data['sort']
            if sort_opt != 'not_sort':
                if form.cleaned_data['order'] == 'asc':
                    books = books.order_by(sort_opt)
                elif form.cleaned_data['order'] == 'desc':
                    books = books.order_by('-'+sort_opt)
            else:
                pass
            
            try:
                books = books.all()
                form = QueryBook()
                return render(request, 'main/queryBook.html', context={'books': books, 'form': form})
            except:
                pass
    books = Book.objects.all()
    form = QueryBook()
    return render(request, 'main/queryBook.html', context={'books': books, 'form': form})

