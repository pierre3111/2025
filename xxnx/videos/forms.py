from django import forms
from .models import Media, Comment
from django.contrib.auth.models import User

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'file', 'media_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
