from django import forms
from .models import MediaUpload, ViewerEmail

class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = MediaUpload
        fields = ['title', 'file']

class EmailForm(forms.ModelForm):
    class Meta:
        model = ViewerEmail
        fields = ['email']
