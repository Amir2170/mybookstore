from django.db import models
from matplotlib.pyplot import cla
from django.core.validators import MaxValueValidator, MinValueValidator # for rate field validation
from django.contrib.auth import get_user_model

# MY IMPORTS


class Review(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,
    )
    rate = models.IntegerField(
        default="0",
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ],
    )
    book = models.ForeignKey(
        'home.Book', 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )