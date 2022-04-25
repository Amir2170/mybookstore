from unicodedata import category, name
from django.test import TestCase
from matplotlib.pyplot import cla, text, title
from django.contrib.auth import get_user_model

#MY IMPORTS
from home.models import Book, Category
from rating.models import Review

# accessing user model
User = get_user_model()


class BookModelTest(TestCase):

    def setUp(self):
        self.book1 = Book.objects.create(
            title="book1",
            text="this is book1"
        )
        self.book2 = Book.objects.create(
            title="book2",
            text="this is book2"
        )
        

    def test_saving_and_retrieving_books(self):
        saved_books = Book.objects.all()

        self.assertEqual(saved_books.count(), 2)

        self.assertEqual(saved_books[0].title, 'book1')
        self.assertEqual(saved_books[1].text, 'this is book2')


    def test_books_can_have_categories(self):
        self.book1.categories.create(name="category1")
        self.book1.categories.create(name="category2")
        
        book_categories = self.book1.categories.all()

        self.assertEqual(book_categories.count(), 2)


    def test_book_model_generate_slug_on_save(self):
        self.assertEqual(self.book1.slug, 'book1')
    

    def test_book_object_string_representation(self):
        self.assertEqual(str(self.book1), 'book1')

    
    def test_book_model_average_review_function(self):
        user = User.objects.create()
        Review.objects.create(
            rate=3,
            book=self.book1,
            user=user,
        )
        Review.objects.create(
            rate=5,
            book=self.book1,
            user=user
        )

        self.assertEqual(
            self.book1.average_review,
            4
        )
        
    


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="my category")


    def test_model_string_representation(self):
        self.assertEqual(str(self.category), "my category")


    def test_slug_field_is_created_from_name(self):
        self.assertEqual(self.category.slug, 'my-category')

    
    # i'm gonna change the object name here, hence putting this test last
    def test_if_slug_is_only_created_upon_creating_object(self): 
        self.category.name = 'your category'
        self.category.save()

        self.assertEqual(self.category.name, 'your category')
        self.assertEqual(self.category.slug, 'my-category')

