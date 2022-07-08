from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm


# MY IMPORTS
from rating.models import Review



class RatingForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['rate', 'user', 'book']