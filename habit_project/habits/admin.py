from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'time', 'periodicity', 'duration', 'is_public')
    list_filter = ('is_public', 'is_pleasant', 'periodicity')
    search_fields = ('action', 'user__email')
