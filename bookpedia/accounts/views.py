from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm
)
from django.views.decorators.http import require_POST


# USER MODEL
User = get_user_model()

# MY IMPORTS
from home.models import Book
from .forms import CustomUserCreationForm



@require_POST
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({'success': True})

        else:
            return JsonResponse(dict(form.errors), status=400) # send a 400 status in case of error

    return HttpResponseNotAllowed(['POST']) # Do not allow GET response at all
                                            # decorator wroks but here just to make sure


@require_POST
def user_creation(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )

            # Login user afterward
            login(request, user)

            return JsonResponse({}, status=200)
        else:
            return JsonResponse(dict(form.errors), status=400) # send a 400 status in case of error

    return HttpResponseNotAllowed(['POST']) # Do not allow GET response at all
                                            # decorator wroks but here just to make sure


@require_POST
def user_change(request):
    form = UserChangeForm(data=request.POST)

    if form.is_valid():
        return JsonResponse({})

    else:
        return JsonResponse({}, status=400)

    return JsonResponse({})

#class CustomLoginView(auth_views.LoginView):
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        current_site = get_current_site(self.request)
#
#        # All books
#        books = Book.objects.all()
#
#        # My code in order to add recommended books to login context
#        recom_books = Book.objects.filter(recommend=True)
#        if not recom_books:
#            recom_books = Book.objects.all()[:5]
#
#        context.update({
#            self.redirect_field_name: sel`f.get_redirect_url(),
#            "site": current_site,
#            "site_name": current_site.name,
#            "recommended_books": recom_books,
#            "books": books,
#            **(self.extra_context or {}),
#        })
#
#        return context
