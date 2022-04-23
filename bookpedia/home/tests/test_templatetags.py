from django.test import TestCase
from matplotlib.pyplot import title

# MY IMPORTS
from home.templatetags.list_index import index
from home.models import Book


class IndexFilterTest(TestCase):

    def setUp(self):
        self.book1 = Book.objects.create(title="book1")
        Book.objects.create(title="book2")
        Book.objects.create(title="book3")
        self.books = Book.objects.all()


    def test_index_filter_returns_index_of_al_element_plus_one(self):
        result = index(self.book1, self.books)
        self.assertEqual(result, 1)