from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_media, name='upload_media'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete/<int:pk>/', views.delete_media, name='delete_media'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]
