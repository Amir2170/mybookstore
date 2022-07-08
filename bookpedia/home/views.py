from django.shortcuts import render
from django.http import FileResponse
from django.core.paginator import Paginator
import random

# MY IMPORTS
from home.models import Book, Category



#Home Page

def home(request):
    # page pagination; put 6 books per page
    all_books = Book.objects.order_by('text')
    paginator = Paginator(all_books, 6)

    page_number = request.GET.get('page')

    # get books for specified page in get request
    books = paginator.get_page(page_number)
    
    recom_books = Book.objects.filter(recommend=True) #Recommended Books
    if not recom_books:
        recom_books = books[:5] #if there is not recommended books slice first five of normal books

    categories = Category.objects.all()[:5] # If categories are more than 5, slice first five and use them
    
    return render(request, 'home_index.html', {
        'books': books, 
        'recommended_books': recom_books,
        'categories': categories,
    })


# Book Details

def book_detail(request, slug):
    book = Book.objects.get(slug=slug)
    book_categories = Category.objects.filter(books=book)

    # Getting a random category from books categories
    # if there is not any categories related to the 
    # specified book return None instead so we can
    # use an if statement in our templates for testing  
    # its existent
    similar_books = None  
    # random_category
    if book_categories.exists():
        rand_category = random.choice(book_categories)
        # filter books according to random cat and exclude the book itself
        similar_books = Book.objects.filter(categories=rand_category).exclude(title=book.title)[:5]
     
    return render(request, 'book_detail.html',{
        'book': book,
        'similar_books': similar_books,
    })


# Category 

def book_category(request, slug):
    pass


# Downlaoding a book

def book_download(request, slug):
    
    book = Book.objects.get(slug=slug)

    return FileResponse(
        open(book.file.path, 'rb'),
        as_attachment=True,
        filename=book.slug + '.pdf'
    )