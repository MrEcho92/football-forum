from django import forms
from forum.models import Post, Comment, Report

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text','image' )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ('text',)


class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        fields = ('message',)
