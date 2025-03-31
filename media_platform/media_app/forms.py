from django import forms
from .models import MediaItem, UserEmail

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'description', 'file', 'media_type']
        
class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email to view content'})
        }