from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'telegram_chat_id', 'is_staff')
    search_fields = ('email', 'username')
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram', {'fields': ('telegram_chat_id',)}),
    )
