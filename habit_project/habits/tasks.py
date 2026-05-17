from celery import shared_task
from django.conf import settings
import requests


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}


@shared_task
def check_and_send_reminders():
    """Проверка привычек и отправка напоминаний"""
    from django.utils import timezone
    from .models import Habit

    now = timezone.localtime()
    current_time = now.time()

    # Находим привычки, которые нужно выполнить в текущее время
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__telegram_chat_id__isnull=False
    )

    for habit in habits:
        message = f"🔔 <b>Напоминание о привычке!</b>\n\n"
        message += f"Действие: {habit.action}\n"
        message += f"Место: {habit.place}\n"
        message += f"Время на выполнение: {habit.duration} сек."

        if habit.reward:
            message += f"\n\nВознаграждение после выполнения: {habit.reward}"
        elif habit.related_habit:
            message += f"\n\nПосле выполнения можно: {habit.related_habit.action}"

        send_telegram_message.delay(habit.user.telegram_chat_id, message)
