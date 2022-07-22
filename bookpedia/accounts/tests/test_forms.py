from django.test import TestCase
from django.contrib.auth import get_user_model

# My imports
from accounts.forms import ChangeUsername

# User model
User = get_user_model()



class TestChangeUserDetailsForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@user.com"
        )
        self.user.set_password('testpass123')
        self.user.save()
