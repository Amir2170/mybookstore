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


class BookDetailView(TestCase):

    def setUp(self):
        photo = tempfile.NamedTemporaryFile(suffix=".jpg").name # Create an image as a temporary file
        self.book1 = Book.objects.create(
            title="book number 1",
            image=photo
        )
        self.book2 = Book.objects.create(
            title="book number two",
            image=photo
        )


    def test_status_code_for_url_dispatcher(self):
        response = self.client.get(
            reverse(
                'home:book-detail',
                args=[self.book1.slug]
            )
        )

        self.assertEqual(response.status_code, 200)

    
    def test_detail_view_context(self):
        category1 = Category.objects.create(name='category1')
        category2 = Category.objects.create(name='category2')
        category3 = Category.objects.create(name='category3')

        self.book1.categories.set([category1, category2, category3])
        # the logic is that i add the same categories as my main book 
        # to this book as well and i check if only this book exists in 
        # context similar books if so then recommeding wroks otherwsie not
        # because picking category is completely random i had no other choice
        self.book2.categories.set([category1, category2, category3])

        # i did this in order to campare a query set version of this to 
        # response similar_books context value which is a queryset
        book2_query = Book.objects.filter(title='book number two') 

        response = self.client.get(
            reverse('home:book-detail', args=[self.book1.slug])
        )

        self.assertEqual(response.context['book'], self.book1)
        self.assertQuerysetEqual(
            response.context['similar_books'],
            book2_query
        )

        # here i dissociate all relations of my second book to simliar
        # categories in order to test whether context similar books will
        # be empty or not
        self.book2.categories.clear()

        response = self.client.get(
            reverse('home:book-detail', args=[self.book1.slug])
        )

        self.assertFalse(
            response.context['similar_books']
        )

    
    def test_recommending_view_doesn_not_send_more_than_five_books(self):
        category1 = Category.objects.create(name='category1')
        category2 = Category.objects.create(name='category2')
        category3 = Category.objects.create(name='category3')

        self.book1.categories.set([category1, category2, category3])

        # Creating 10 different books with same categories
        photo = tempfile.NamedTemporaryFile(suffix=".jpg").name # Create an image as a temporary file
        for i in range(10):
            book = Book.objects.create(
                title=f'book {i}',
                image=photo,
            )
            book.categories.set([category1, category2, category3])

        response = self.client.get(
            reverse('home:book-detail', args=[self.book1.slug])
        )

        books_to_exclude = ['book number 1','book number two'] # Titles of the books to exclude
        similar_books = Book.objects.exclude(title__in=books_to_exclude)[:5]

        self.assertQuerysetEqual(
            response.context['similar_books'],
            similar_books,
            ordered=False
        )