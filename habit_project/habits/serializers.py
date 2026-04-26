from rest_framework import serializers
from .models import Habit
from .validators import validate_habit_rules


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action',
            'is_pleasant', 'related_habit', 'periodicity',
            'reward', 'duration', 'is_public', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        return validate_habit_rules(data)