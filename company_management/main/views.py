from smtplib import SMTPException
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .forms import RegistrationForm, LoginForm
from django.core.mail import send_mail
import random

otp_storage = {}  # Temporary in-memory OTP storage

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            otp = random.randint(100000, 999999)
            otp_storage[user.email] = otp
            try:
                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp}',
                    'heifermpc@gmail.com',  # Replace with your email
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Registration successful. Check your email for the OTP.')
                return redirect('otp_verify')
            except SMTPException as e:
                messages.error(request, 'Failed to send OTP email. Please try again later.')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Account not verified. Check your email for OTP.')
                    return redirect('otp_verify')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def otp_verify(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging line
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        print(f"Email: {email}, OTP: {otp}")  # Debugging line

        # Validate email and OTP
        if not email or not otp:
            messages.error(request, 'Email and OTP are required.')
            return redirect('otp_verify')

        try:
            otp = int(otp)  # Convert OTP to integer
        except ValueError:
            messages.error(request, 'Invalid OTP format.')
            return redirect('otp_verify')

        if email in otp_storage and otp_storage[email] == otp:
            try:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                del otp_storage[email]  # Remove OTP from temporary storage
                messages.success(request, 'Account verified. You can now log in.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with the provided email.')
                return redirect('otp_verify')
        else:
            messages.error(request, 'Invalid OTP or email.')
            return redirect('otp_verify')

    return render(request, 'main/otp_verify.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
