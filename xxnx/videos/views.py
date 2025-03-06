from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Media, Comment
from .forms import MediaForm, CommentForm, CustomUserCreationForm, CustomLoginForm

# =============================
# Media (Video/Photo) Management Views
# =============================

def video_list(request):
    media = Media.objects.all().order_by('-uploaded_at')
    return render(request, 'video_list.html', {'media': media})

def video_detail(request, pk):
    media = get_object_or_404(Media, pk=pk)
    comments = media.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.media = media
            comment.user = request.user
            comment.save()
            return redirect('video_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'video_detail.html', {'media': media, 'comments': comments, 'form': form})

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.uploaded_by = request.user
            media.save()
            return redirect('video_list')
    else:
        form = MediaForm()

    return render(request, 'upload.html', {'form': form})

@login_required
def admin_dashboard(request):
    media = Media.objects.all()
    return render(request, 'dashboard.html', {'media': media})

@login_required
def delete_media(request, pk):
    media = get_object_or_404(Media, pk=pk)
    media.delete()
    return redirect('admin_dashboard')


# =============================
# Custom User Authentication Views
# =============================

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('video_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('video_list')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')
