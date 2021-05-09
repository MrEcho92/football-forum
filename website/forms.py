from django import forms
from website.models import subscriber

class subscriberForm(forms.ModelForm):
    class Meta:
        model= subscriber
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            return email
