from .models import MusicBlog, Vote
from django import forms

class BlogForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('vote',)