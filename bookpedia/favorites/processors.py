# User favorite books context processor; so i can access user favorites in all templates

from .models import Favorites
from home.models import Book



def usr_favorites(request):
    # if user is authenticated supply queryset if not send an empty queryset 
    # to avoid anonymous user error
    if request.user.is_authenticated:
        usr_favs = Book.objects.filter(favorites__user=request.user)
    else:
        usr_favs = Favorites.objects.none()

    return {
        'usr_favs': usr_favs,
    }