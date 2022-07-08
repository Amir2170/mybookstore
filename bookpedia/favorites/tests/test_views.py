from django.test import TestCase
from django.contrib.auth import get_user_model
from tempfile import NamedTemporaryFile
from django.urls import reverse


# MY IMPORTS
from favorites.models import Favorites
from home.models import Book


# User model
User = get_user_model()



class AddBookTest(TestCase):
    def setUp(self):
        photo = NamedTemporaryFile(suffix='.jpg').name
        self.book1 = Book.objects.create(
            title='book1',
            image=photo
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com'
        )
        self.user.set_password('testpass')
        self.user.save()
        # Log created user in
        self.client.login(username='testuser', password='testpass')


    def test_view_returns_appropriate_json_response_if_user_is_not_authenticated(self):
        self.client.logout()
        response = self.client.post(reverse('favorites:add-book', args=[self.book1.slug]))

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'success': False, 'error': 'user is not autneticated'}
        )

    
    def test_view_returns_appropriate_json_response_if_book_already_exists_in_user_favorite_list(self):
        self.client.post(reverse('favorites:add-book', args=[self.book1.slug]))
        response = self.client.post(reverse('favorites:add-book', args=[self.book1.slug]))

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'success': False, 'error': 'book already exists in list'}
        )

    
    def test_favorite_obj_is_created_if_not_there_and_corresponding_book_gets_associated_with(self):
        response = self.client.post(reverse('favorites:add-book', args=[self.book1.slug]))

        favorite_obj = Favorites.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorites.objects.count(), 1) # test how many objects area created
        self.assertEqual(favorite_obj.books.count(), 1) # test relationships
        self.assertEqual(favorite_obj.books.first().title, 'book1') # test book saved

    
    def test_book_gets_associated_with_list_if_list_already_exists(self):
        favorite_obj = Favorites.objects.create(user=self.user)

        response = self.client.post(reverse('favorites:add-book', args=[self.book1.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorites.objects.count(), 1) # test how many objects area created
        self.assertEqual(favorite_obj.books.count(), 1) # test relationships
        self.assertEqual(favorite_obj.books.first().title, 'book1') # test book saved



class RemoveBookViewTest(TestCase):
    def setUp(self):
        photo = NamedTemporaryFile(suffix='jpg').name
        self.book1 = Book.objects.create(
            image=photo,
            title="book1",
        )

        # user creation and setting password + logging user in

        self.user = User.objects.create(
            username='testuser',
            email='test@user.com'
        )

        self.user.set_password('testpass')
        self.user.save()

        self.client.login(
            username="testuser",
            password='testpass',
        )

        # add book to user favorites
        self.client.post(reverse('favorites:add-book', args=[self.book1.slug]))


    def test_view_only_accepts_post_requests(self):
        response = self.client.get(reverse('favorites:remove-book', args=[self.book1.slug]))

        self.assertEqual(response.status_code, 405)

    
    def test_post_request_successfully_remove_book_from_user_favs_and_returns_proper_json_response(self):
        # first check if there is really a favorite list and book1 is in it
        usr_favs = Favorites.objects.get(user=self.user)
        book = Book.objects.get(favorites=usr_favs)
        self.assertEqual(book.title, 'book1')

        response = self.client.post(reverse('favorites:remove-book', args=[self.book1.slug]))

        self.assertEqual(response.status_code, 200)
        
        # check if book is removed using assertRaises as context manager
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(favorites=usr_favs)

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'success': True}
        )

    