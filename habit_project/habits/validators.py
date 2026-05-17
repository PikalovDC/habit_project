from rest_framework.exceptions import ValidationError


def validate_habit_rules(data):
    """
    Валидация правил для привычек:
    1. Нельзя одновременно выбрать связанную привычку и вознаграждение
    2. В связанные привычки могут попадать только привычки с признаком приятной привычки
    3. У приятной привычки не может быть вознаграждения или связанной привычки
    """
    related_habit = data.get('related_habit')
    reward = data.get('reward')
    is_pleasant = data.get('is_pleasant')

    # Правило 1: нельзя одновременно related_habit и reward
    if related_habit and reward:
        raise ValidationError(
            'Нельзя одновременно указывать связанную привычку и вознаграждение'
        )

    # Правило 2: связанная привычка должна быть приятной
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError(
            'Связанная привычка должна быть приятной'
        )

    # Правило 3: у приятной привычки не может быть reward или related_habit
    if is_pleasant and (reward or related_habit):
        raise ValidationError(
            'Приятная привычка не может иметь вознаграждение или связанную привычку'
        )

    return data
