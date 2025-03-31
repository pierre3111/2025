from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import MediaItem, UserEmail, MediaAccess
from .forms import MediaItemForm, UserEmailForm

def is_admin(user):
    return user.is_staff or user.is_superuser

# Public views
def home_view(request):
    media_items = MediaItem.objects.all().order_by('-uploaded_at')
    context = {
        'media_items': media_items,
    }
    return render(request, 'media_app/home.html', context)

def submit_email_view(request, media_id):
    media_item = get_object_or_404(MediaItem, id=media_id)
    
    if request.method == 'POST':
        form = UserEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Get or create user email
            user_email, created = UserEmail.objects.get_or_create(
                email=email,
                defaults={'access_count': 1}
            )
            
            # If not created, increment access count
            if not created:
                user_email.access_count += 1
                user_email.save()
                
            # Record this specific media access
            MediaAccess.objects.get_or_create(
                user_email=user_email,
                media_item=media_item
            )
            
            # Store email in session
            request.session['user_email'] = email
            
            return redirect('media_detail', media_id=media_id)
    else:
        form = UserEmailForm()
        
    context = {
        'form': form,
        'media_item': media_item,
    }
    return render(request, 'media_app/email_form.html', context)

def media_detail_view(request, media_id):
    media_item = get_object_or_404(MediaItem, id=media_id)
    
    # Check if there's a record in MediaAccess for this session
    email = request.session.get('user_email', None)
    if not email:
        return redirect('submit_email', media_id=media_id)
    
    try:
        user_email = UserEmail.objects.get(email=email)
        media_access = MediaAccess.objects.filter(
            user_email=user_email,
            media_item=media_item
        ).exists()
        
        if not media_access:
            return redirect('submit_email', media_id=media_id)
    except UserEmail.DoesNotExist:
        return redirect('submit_email', media_id=media_id)
    
    context = {
        'media_item': media_item,
    }
    return render(request, 'media_app/media_detail.html', context)

# Admin views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    media_items = MediaItem.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    context = {
        'media_items': media_items,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def create_media_view(request):
    if request.method == 'POST':
        form = MediaItemForm(request.POST, request.FILES)
        if form.is_valid():
            media_item = form.save(commit=False)
            media_item.uploaded_by = request.user
            media_item.save()
            messages.success(request, 'Media uploaded successfully!')
            return redirect('admin_dashboard')
    else:
        form = MediaItemForm()
    
    context = {
        'form': form,
        'form_title': 'Upload New Media',
    }
    return render(request, 'admin/media_form.html', context)

@login_required
@user_passes_test(is_admin)
def update_media_view(request, media_id):
    media_item = get_object_or_404(MediaItem, id=media_id)
    
    # Only allow the uploader or superusers to edit
    if media_item.uploaded_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this media")
    
    if request.method == 'POST':
        form = MediaItemForm(request.POST, request.FILES, instance=media_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = MediaItemForm(instance=media_item)
    
    context = {
        'form': form,
        'form_title': 'Update Media',
        'media_item': media_item,
    }
    return render(request, 'admin/media_form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_media_view(request, media_id):
    media_item = get_object_or_404(MediaItem, id=media_id)
    
    # Only allow the uploader or superusers to delete
    if media_item.uploaded_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this media")
    
    if request.method == 'POST':
        media_item.delete()
        messages.success(request, 'Media deleted successfully!')
        return redirect('admin_dashboard')
    
    context = {
        'media_item': media_item,
    }
    return render(request, 'admin/confirm_delete.html', context)

@login_required
@user_passes_test(is_admin)
def user_emails_view(request):
    user_emails = UserEmail.objects.all().order_by('-submitted_at')
    context = {
        'user_emails': user_emails,
    }
    return render(request, 'admin/user_emails.html', context)