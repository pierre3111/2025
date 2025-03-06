from django.shortcuts import render, redirect, get_object_or_404
from .models import MediaUpload, ViewerEmail
from .forms import MediaUploadForm, EmailForm

# Admin Dashboard (Manage Uploads and Emails)
def dashboard(request):
    media = MediaUpload.objects.all()
    emails = ViewerEmail.objects.all()
    return render(request, 'media_app/dashboard.html', {'media': media, 'emails': emails})

# Upload Media (Admin Only)
def upload_media(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MediaUploadForm()
    return render(request, 'media_app/upload.html', {'form': form})

# Delete Media (Admin Only)
def delete_media(request, pk):
    media = get_object_or_404(MediaUpload, pk=pk)
    if request.method == 'POST':
        media.delete()
        return redirect('dashboard')
    return redirect('dashboard')

# User Email Collection
def collect_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()  # Save the email every time
            return redirect('main_gallery')  # Redirect to gallery after submission
    else:
        form = EmailForm()

    return render(request, 'media_app/email_form.html', {'form': form})

# Main Page for Users (after email submission)
def main_gallery(request):
    if not request.session.get('email_submitted'):
        return redirect('collect_email')

    media = MediaUpload.objects.all()
    return render(request, 'media_app/main_gallery.html', {'media': media})


