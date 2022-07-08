from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from home.models import Book


# MY IMPORTS
from .models import Favorites



@require_POST
def add_book(request, slug):
    # Check if user is logged if, error otherwise
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'user is not autneticated'}, status=401)
    
    favorite, created = Favorites.objects.get_or_create(user=request.user)
    book = Book.objects.get(slug=slug)

    if favorite.books.contains(book): # i have handled this situation in my templates, added this just to make sure.
        return JsonResponse({'success': False, 'error': 'book already exists in list'}, status=400)

    favorite.books.add(book)
    return JsonResponse({'success': True}, status=200)
    

@require_POST
def remove_book(request, slug):
    # since if user is not authenticated processor will send 
    # an empty queryset to templates there is no need to handle 
    # unauthenticated user situation

    # so first get specified book and current user favorite list
    book = Book.objects.get(slug=slug)
    usr_favorites = Favorites.objects.get(user=request.user)

    usr_favorites.books.remove(book)

    return JsonResponse({'success': True}, status=200) 

    