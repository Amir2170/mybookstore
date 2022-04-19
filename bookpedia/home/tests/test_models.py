from unicodedata import category, name
from django.test import TestCase
from matplotlib.pyplot import cla, text, title

#MY IMPORTS
from home.models import Book, Category


class BookModelTest(TestCase):

    def test_saving_and_retrieving_books(self):
        book1 = Book.objects.create(
            title="book1",
            text="this is book1"
        )
        book2 = Book.objects.create(
            title="book2",
            text="this is book2"
        )

        saved_books = Book.objects.all()

        self.assertEqual(saved_books.count(), 2)

        self.assertEqual(saved_books[0].title, 'book1')
        self.assertEqual(saved_books[1].text, 'this is book2')


    def test_books_can_have_categories(self):
        book = Book.objects.create(
            title="book"
        )
        book.categories.create(name="category1")
        book.categories.create(name="category2")
        
        book_categories = book.categories.all()

        self.assertEqual(book_categories.count(), 2)


    def test_book_model_generate_slug_on_save(self):
        book = Book.objects.create(title="book title")

        self.assertEqual(book.slug, 'book-title')
    

    def test_book_object_string_representation(self):
        book = Book.objects.create(title="book")
        
        self.assertEqual(str(book), 'book')
    
    