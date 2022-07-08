from math import fabs
from urllib import response
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
import sweetify


# MY IMPORTS 
from home.models import Book
from .forms import RatingForm
from .models import Review


# USER MODEL
User = get_user_model()



@require_POST
def rate_book(request, book_slug):
    # Check if user is logged in, error if not
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'user not authenticated'}, status=401)

    # Check if user has voted before and error if he/she did
    try:
        book = Book.objects.get(slug=book_slug)
        Review.objects.get(
            user=request.user,
            book=book 
        )
    # Check if book exists with the specified slug exists in db, error if not
    except Book.DoesNotExist:
        return JsonResponse(
            {'success': False, 'error': 'book does not exists'}, 
            status=400
        )
    # now that book exists check if user has voted that book if not continue
    except Review.DoesNotExist:
        if request.method == 'POST':
            form = RatingForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.book = book
                
                # now it's time to save the actual rating
                if 'one' in request.POST:
                    review.rate = 1
                elif 'two' in request.POST:
                    review.rate = 2
                elif 'three' in request.POST:
                    review.rate = 3
                elif 'four' in request.POST:
                    review.rate = 4
                else:
                    review.rate = 5
                
                review.save()
                form.save_m2m() # I don't have any m2m relation, this is here
                                # just to make sure if there will be any m2m in future
                return JsonResponse({'success': True, 'title': book.title})
            else:            
                return JsonResponse({'sucess': False, 'error': 'invlaid form'}, status=400)
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        return JsonResponse({'success': False, 'error': 'user voted before'}, status=423)