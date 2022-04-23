from cgitb import html
from unicodedata import category
from django.shortcuts import render

# MY IMPORTS
from home.models import Book, Category



#Home Page

def home(request):
    books = Book.objects.all()
    
    recom_books = Book.objects.filter(recommend=True) #Recommended Books
    if not recom_books:
        recom_books = books[:5] #if there is not recommended books slice first five of normal books

    categories = Category.objects.all()[:5] # If categories are more than 5, slice first five and use them
    
    return render(request, 'home_index.html', {
        'books': books, 
        'recommended_books': recom_books,
        'categories': categories,
    })


