from django.contrib.auth.forms import ( 
    AuthenticationForm, 
    UserCreationForm, 
    UserChangeForm,
)

def auth_forms(request):
    return {
        'login_form': AuthenticationForm(),
        'user_creation_form': UserCreationForm(),
        'user_change_form': UserChangeForm(),
    }