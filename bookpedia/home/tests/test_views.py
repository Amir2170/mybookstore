from unicodedata import category, name
from django.test import TestCase
from urllib import response
from xmlrpc import client
from matplotlib.pyplot import cla, title
from django.urls import reverse
import tempfile

#MY IMPORTS
from ..models import Book, Category


class HomeViewtest(TestCase):
    
    def setUp(self):
        photo = tempfile.NamedTemporaryFile(suffix=".jpg").name # Create an image as a temporary file
        self.book1 = Book.objects.create(
            title="book1",
            recommend=True,
            image=photo
        )
        self.book2 = Book.objects.create(
            title="book2",
            image=photo
        )
        Book.objects.create(
            title="book3",
            image=photo
        )
        Book.objects.create(
            title="book4",
            image=photo
        )
        Book.objects.create(
            title="book5",
            image=photo
        )


    def test_root_url_resolves_to_home_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    
    def test_view_uses_right_template(self):
        response = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(response, 'home.html')

    
    def test_view_sends_all_books_to_template(self):
        response = self.client.get(reverse('home:index'))
        books = Book.objects.all()

        self.assertQuerysetEqual(
            response.context['books'], 
            books,
            ordered=False,
        )
    
    
    def test_view_sends_recommended_books_to_template(self):
        response = self.client.get(reverse('home:index'))
        recom_book = Book.objects.filter(recommend=True)

        self.assertQuerysetEqual(
            response.context['recommended_books'],
            recom_book,
            ordered=False,
        )
    
    
    def test_if_no_recommended_books_is_available_normal_books_replaces_them(self):
        self.book1.recommend = False
        self.book1.save()
        books = Book.objects.all()

        response = self.client.get(reverse('home:index'))

        self.assertQuerysetEqual(
            response.context['recommended_books'],
            books,
            ordered=False,
        )
    

    # Just want to make sure if there are less than five books in database
    # home view works regardless
    def test_home_view_works_for_reccommend_if_4_books_are_available(self):
        self.book2.delete()
        self.book1.recommend = False
        self.book1.save()
        books = Book.objects.all()

        response = self.client.get(reverse('home:index'))

        self.assertQuerysetEqual(
            response.context['recommended_books'],
            books,
            ordered=False
        )

    
    def test_home_view_categories(self):
        for i in range(5):
            Category.objects.create(name=f'category{i}')
        
        categories = Category.objects.all()

        response = self.client.get(reverse('home:index'))

        self.assertQuerysetEqual(
            response.context['categories'],
            categories,
            ordered=False
        )