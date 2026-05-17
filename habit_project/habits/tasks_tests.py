from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch, MagicMock
from .models import Habit
from .tasks import send_telegram_message, check_and_send_reminders

User = get_user_model()


class CeleryTasksTest(TestCase):
    """Тесты для Celery задач"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru',
            username='test',
            password='testpass123',
            telegram_chat_id='123456789'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=timezone.localtime().time(),
            action='Тестовая привычка',
            duration=60
        )

    @patch('habits.tasks.requests.post')
    def test_send_telegram_message_success(self, mock_post):
        """Тест: успешная отправка Telegram сообщения"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ok': True}
        mock_post.return_value = mock_response

        result = send_telegram_message('123456789', 'Тест')

        self.assertEqual(result['ok'], True)
        mock_post.assert_called_once()

    @patch('habits.tasks.send_telegram_message.delay')
    def test_check_and_send_reminders(self, mock_send):
        """Тест: проверка и отправка напоминаний"""
        mock_send.return_value = None

        result = check_and_send_reminders()

        self.assertIsNotNone(result)
