from audioop import avg
from email.policy import default
from unicodedata import category, name
from django.db import models
from matplotlib.pyplot import text, title
from django.core.validators import MaxValueValidator, MinValueValidator #For validating book score
from django.template.defaultfilters import slugify #To slugify title
from django.db.models import Avg


# MY IMPORTS
from rating.models import Review



class Category(models.Model):
    name = models.CharField(max_length=200, default="")
    slug = models.SlugField(default="", unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:     # Slugify only once when object is created, don't want broken links
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)



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
    file = models.FileField(
        upload_to='home/uploads/%Y/%m/%d',
        default="",
    )
    rating = models.IntegerField(default=0, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    author = models.CharField(max_length=100, default="")
    recommend = models.BooleanField(default=False)

    @property
    def average_review(self):
        reviews = Review.objects.filter(book=self).aggregate(avg_rate=Avg('rate'))
        avg = 0
        
        if reviews['avg_rate'] is not None:
            avg = float(reviews['avg_rate'])
        
        return avg


    def save(self, *args, **kwargs): # Overriding save method to generate 
        self.slug = slugify(self.title) # an editable slug on saving
        super().save(*args, **kwargs) 


    def __str__(self):
        return self.title
    