from django.test import TestCase
from django.contrib.auth import get_user_model
from matplotlib.pyplot import title

# MY IMPORTS
from .models import Review
from home.models import Book

# SPECIFYING USER MODEL
User = get_user_model()


class ReviewModelTest(TestCase):
    def test_review_model_creation(self):
        book1 = Book.objects.create(title="book1")
        book2 = Book.objects.create(title="book2")
        user = User.objects.create()
        review1 = Review.objects.create(
            user=user,
            rate=3,
            book=book1,
        )
        review2 = Review.objects.create(
            user=user,
            rate=3,
            book=book2,
        )

        reviews = Review.objects.all()

        self.assertEqual(reviews[0], review1)
        self.assertEqual(reviews[1], review2)