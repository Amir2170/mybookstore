from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model


# MY IMPORTS
from home.models import Book


# USER MODEL 
User = get_user_model()



class Favorites(models.Model):
    books = models.ManyToManyField(Book) # Can be empty in db, for when obj is created
    user = models.OneToOneField(User, on_delete=models.CASCADE) # if user obj is deleted, delete this obj as well