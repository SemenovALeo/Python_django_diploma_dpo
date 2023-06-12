from django.contrib import admin
from .models import Profile, Image

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'full_name', 'avatar']
    raw_id_fields = ['user']

@admin.register(Image)
class ProfileAvatar(admin.ModelAdmin):
    list_display = ['avatar', 'alt_text']