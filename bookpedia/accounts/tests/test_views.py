import email
from urllib import response
from django.test import TestCase
from django.urls import reverse
import tempfile
from django.contrib.auth import get_user_model

# MY IMPORTS
from home.models import Book, Category


# User object
User = get_user_model()


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@user",
        )
        self.user.set_password('testpass')
        self.user.save()


    def test_login_view_only_accepts_post_requests(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 405)



    def test_login_view_sends_form_errors_and_uses_right_status_in_case_of_invalid_form(self):
        response = self.client.post(reverse('accounts:login'), data={
            'username': 'testuser1', #invalid username
            'password': 'testpass',
        })
 
        self.assertJSONEqual(
            response.content.decode('utf8'),
            {"__all__": ["Please enter a correct username and password. "
            "Note that both fields may be case-sensitive."]}
        )
        self.assertEqual(response.status_code, 400)


    def test_login_view_log_user_in_and_sends_json_response(self):
        response = self.client.post(reverse('accounts:login'), data={
            'username': 'testuser', #valid username
            'password': 'testpass',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    
    



#class CustomLoginView(TestCase):

#    def setUp(self):
#        photo = tempfile.NamedTemporaryFile(suffix=".jpg").name # Create an image as a temporary file
#        self.book1 = Book.objects.create(
#            title="book1",
#            recommend=True,
#            image=photo
#        )
#        self.book2 = Book.objects.create(
#            title="book2",
#            image=photo
#        )
    

#    def test_cutom_login_view_sends_recommended_books_to_template_in_context(self):
#        response = self.client.get(reverse('accounts:login'))

#        recom_books = Book.objects.filter(recommend=True)

#        self.assertQuerysetEqual(
#            response.context['recommended_books'],
#            recom_books,
#            ordered=False
#        )
    
    # Here i test bookpedia.processors file and check if it add login form to all contexes
#    def test_if_auth_form_exists_in_all_views_context(self):
#        response1 = self.client.get(reverse('home:index'))
#        response2 = self.client.get(
#            reverse('home:book-detail',
#            args=[self.book1.slug]
#        ))
#        self.assertIn('login_form', response1.context)
#        self.assertIn('login_form', response2.context)


#    def test_if_user_gets_redirect_to_home_page_after_successfully_logging_in(self):
#        User.objects.create_user(
#            username="testuser",
#            email="test@user",
#            password='testpass',
#        )

#        response = self.client.post(reverse('accounts:login'), data=
#            {'username': 'testuser', 'password': 'testpass'}
#        )
#        self.assertRedirects(response, reverse('home:index'))

        

class LogoutViewTest(TestCase):

    def test_view_successfully_redirects_to_home_page(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@user",
        )
        user.set_password('testpass')
        user.save()

        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('accounts:logout'))

        self.assertRedirects(response, reverse('home:index'))



class UserCreationViewTest(TestCase):
    
    def test_view_only_works_with_post_requests(self):
        response = self.client.get(reverse('accounts:user-creation'))
        self.assertEqual(response.status_code, 405)


    def test_view_sends_form_errors_and_right_status_code_in_case_of_errors(self):
        response = self.client.post(reverse('accounts:user-creation'), data={
            'username': 'testuser',
            'password1': 'testpass1',
            'password2': 'testpass2',
        })

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {"password2": ['The two password fields didn’t match.']}
        )

        self.assertEqual(response.status_code, 400)

    
    def test_view_creates_user_object_with_specified_details(self):
        response = self.client.post(reverse('accounts:user-creation'), data= {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })

        self.assertEqual(User.objects.count(), 1)

        self.assertEqual(response.status_code, 200)

    
    def test_created_user_logs_in_afterward(self):
        response = self.client.post(reverse('accounts:user-creation'), data= {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)



class UserChangeViewTest(TestCase):

    def test_view_only_accepts_post_requets(self):
        response = self.client.get(reverse('accounts:user-change'))

        self.assertEqual(response.status_code, 405)

 
    def test_view_returns_400_status_code_in_case_of_invalid_data(self):
        response = self.client.post(reverse('accounts:user-change'))

        self.assertEqual(response.status_code, 400)