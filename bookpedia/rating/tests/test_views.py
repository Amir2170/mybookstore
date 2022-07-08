from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import tempfile
from matplotlib import image

from matplotlib.pyplot import title

# MY IMPORTS
from home.models import Book
from rating.models import Review

# MY USER MODEL
User = get_user_model()



class TestRateBookView(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@email"
        )
        self.user.set_password('testpass')
        self.user.save()
        self.client.login(
            username="testuser",
            password="testpass"
        )
        photo = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.book1 = Book.objects.create(
            title="book1",
            recommend=True,
            image=photo
        )
        self.book2 = Book.objects.create(
            title="book2",
            image=photo
        )

    
    def test_view_creates_a_review_and_bind_the_right_book_to_it(self):
        self.client.post(reverse('review:rate', args=[self.book1.slug]))

        self.assertTrue(Review.objects.get(book=self.book1))

    
    def test_created_review_is_related_to_the_right_book_and_user(self):
        self.client.post(reverse('review:rate', args=[self.book1.slug]))

        review1 = Review.objects.get(book=self.book1)
        self.assertEqual(review1.user, self.user)
        self.assertEqual(review1.book, self.book1)


    def test_if_view_rate_the_book_correctly_according_to_data_one(self):
        self.client.post(reverse('review:rate', args=[self.book1]), data={
            'one': 'one',
        })

        review1 = Review.objects.get(book=self.book1)

        self.assertEqual(review1.rate, 1)


    def test_book_name_is_returned_as_a_json_response_after_rating(self):
        response = self.client.post(reverse('review:rate', args=[self.book1.slug]), data={
            'one': 'one',
        })

        # checking status code first
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {"success": True, "title": "book1"}
        )

    
    def test_only_post_request_works_with_this_view(self):
        response = self.client.get(reverse('review:rate', args=[self.book1.slug]))
        self.assertEqual(response.status_code, 405)

    
    def test_if_book_does_not_exists_view_returns_correct_json_response(self):
        response = self.client.post(reverse('review:rate', args=['book12']))
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'success': False, 'error': 'book does not exists'}
        )

    
    def test_user_cannot_vote_the_same_book_two_times(self):
        self.client.post(reverse('review:rate', args=[self.book1.slug]))
        respone = self.client.post(reverse('review:rate', args=[self.book1.slug]))

        self.assertEqual(respone.status_code, 423)
        self.assertJSONEqual(
            respone.content.decode('utf-8'),
            {'success': False, 'error': 'user voted before'}
        )

    
    def test_user_can_rate_two_different_books(self):
        response = self.client.post(reverse('review:rate', args=[self.book1.slug]))

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {"success": True, "title": "book1"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('review:rate', args=[self.book2.slug]))

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {"success": True, "title": "book2"}
        )
        self.assertEqual(response.status_code, 200)
    

    def test_only_login_user_can_vote(self):
        self.client.logout()
        respone = self.client.post(reverse('review:rate', args=[self.book1.slug]))
        
        self.assertEqual(respone.status_code, 401)
        self.assertJSONEqual(
            respone.content.decode('utf-8'),
            {'success': False, 'error': 'user not authenticated'}
        )