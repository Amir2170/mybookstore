from email.policy import default
from unicodedata import category, name
from django.db import models
from matplotlib.pyplot import text, title
from django.template.defaultfilters import slugify #To slugify title


class Category(models.Model):
    name = models.CharField(max_length=200, default="")


class Book(models.Model):
    BOOK_LANGUAGE = [
        ('EN', 'English'),
        ('FR', 'Farsi'),
    ]
    categories = models.ManyToManyField(
        'Category', 
        related_name='books',
        blank=True, # there may be some books without any categories
    )              
    title = models.CharField( 
        max_length=300, 
        unique=True, # Planning to use title as slugfield, hence 'unique = True'
        default="",
    )
    text = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=300, default="")
    language = models.CharField(
        max_length=300, 
        choices=BOOK_LANGUAGE,
        default="",
    )
    image = models.ImageField(
        upload_to="home/%Y/%m/%d/",
        default="",
    )

    def save(self, *args, **kwargs): # Overriding save method to generate 
        self.slug = slugify(self.title) # an editable slug on saving
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title
    