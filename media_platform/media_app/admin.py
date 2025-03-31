from django.contrib import admin
from .models import MediaItem, UserEmail, MediaAccess

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('media_type', 'uploaded_at')
    search_fields = ('title', 'description')

@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'submitted_at', 'last_accessed', 'access_count')
    list_filter = ('submitted_at', 'last_accessed')
    search_fields = ('email',)

@admin.register(MediaAccess)
class MediaAccessAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'media_item', 'accessed_at')
    list_filter = ('accessed_at',)
    search_fields = ('user_email__email', 'media_item__title')