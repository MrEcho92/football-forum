from django import forms
from news.models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        fields =('title', 'slug', 'author','message','image_upload','status', 'league' )
