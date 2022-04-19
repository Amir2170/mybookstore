from cgitb import html
from django.shortcuts import render

#Home Page

def home(request):
    return render(request, 'index.html')


