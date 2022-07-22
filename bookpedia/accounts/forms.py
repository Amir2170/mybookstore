from pyexpat import model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms



# User Model
User = get_user_model()


# Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        help_text=_('Enter a valid email address.')
    )

    class Meta(UserCreationForm.Meta):
        fields = ["username", "email", "password1", "password2",]



class ChangeUserDetails(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email",]


    #tweaking __init__ in order to be able to access current logged in user
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
