from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_gallery, name='main_gallery'),  # Set main gallery as home page
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_media, name='upload_media'),
    path('delete/<int:pk>/', views.delete_media, name='delete_media'),
    path('email/', views.collect_email, name='collect_email'),
    #path('media/', views.view_media, name='view_media'),
]
