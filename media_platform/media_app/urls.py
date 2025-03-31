from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home_view, name='home'),
    path('media/<int:media_id>/', views.media_detail_view, name='media_detail'),
    path('media/<int:media_id>/submit-email/', views.submit_email_view, name='submit_email'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/media/create/', views.create_media_view, name='create_media'),
    path('admin/media/<int:media_id>/update/', views.update_media_view, name='update_media'),
    path('admin/media/<int:media_id>/delete/', views.delete_media_view, name='delete_media'),
    path('admin/user-emails/', views.user_emails_view, name='user_emails'),
]