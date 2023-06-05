from .models import MusicBlog, Vote, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = MusicBlog
        fields = ('title', 'body', 'image',)

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment*'}),
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('vote',)