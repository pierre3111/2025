from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
