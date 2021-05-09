from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import UserProfile
from django_countries.widgets import CountrySelectWidget


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter valid email address. ')
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"

        #Remove help_text on sign up page
        for fieldname in ['username', 'password2']:
            self.fields[fieldname].help_text = None

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "bio", "country","profile_pic" )
        exclude = ['comment_count', 'post_count',]
        widgets = {'country': CountrySelectWidget()}
