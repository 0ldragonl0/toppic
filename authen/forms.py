from django.contrib.auth.models import User
from django.forms import ModelForm,forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email','first_name','last_name']
        help_texts = {
            'username': str('Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.<br><br>'),
            'password': str('<br>'),
            'email': str('<br>'),
            'first_name': str('<br>'),
            'last_name' : str('<br>'),
        }
