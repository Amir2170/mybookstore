import email
from django.test import TestCase
from django.contrib.auth import get_user_model

# MY IMPORTS
from rating.forms import RatingForm
from rating.models import Review


# MY USER
User = get_user_model()



class RatingFormTest(TestCase):

    def test_rating_form(self):
        # Creating user for 
        user = User.objects.create(
            username="testuser",
            email="test@user"
        )
        user.set_password('testpass')
        user.save()

        # Creating Book
