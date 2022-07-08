from pyexpat import model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms




# User Model
User = get_user_model()



class ChangeUsername(forms.Form):
    old_username = UsernameField(help_text=_("Your Old Username That You Want To Change"))