from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from .models import User
from .forms import RegistrationForm, LoginForm
from .utils import generate_otp, is_otp_expired, send_otp_email
import logging

# Temporary in-memory OTP storage
otp_storage = {}

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            otp = generate_otp()
            otp_storage[user.email.lower()] = {'otp': otp, 'timestamp': datetime.now()}
            try:
                send_otp_email(user.email, otp)
                messages.success(request, 'Registration successful. Check your email for the OTP.')
                return redirect('otp_verify')
            except Exception as e:
                logger.error(f"Failed to send OTP email: {e}")
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
            user = authenticate(request, email=email, password=password)  # Validate credentials
            if user:
                if user.is_active:
                    login(request, user)  # Log the user in
                    return redirect('dashboard')  # Redirect to the dashboard
                else:
                    messages.warning(request, 'Account not verified. Check your email for OTP.')
                    return redirect('otp_verify')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def otp_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        otp_input = request.POST.get('otp')

        if not email or not otp_input:
            messages.error(request, 'Email and OTP are required.')
            return redirect('otp_verify')

        try:
            otp_input = int(otp_input)
        except ValueError:
            messages.error(request, 'Invalid OTP format.')
            return redirect('otp_verify')

        if email in otp_storage:
            stored_data = otp_storage[email]
            otp = stored_data['otp']
            timestamp = stored_data['timestamp']

            if is_otp_expired(timestamp):
                del otp_storage[email]
                messages.error(request, 'OTP expired. Please register again.')
                return redirect('register')

            if otp == otp_input:
                try:
                    user = User.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    del otp_storage[email]
                    messages.success(request, 'Account verified. You can now log in.')
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, 'No account found with the provided email.')
            else:
                messages.error(request, 'Incorrect OTP.')
        else:
            messages.error(request, 'No OTP found for this email.')

    return render(request, 'main/otp_verify.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
