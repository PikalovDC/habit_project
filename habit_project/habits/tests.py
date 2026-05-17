from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import time
from .models import Habit
from .serializers import HabitSerializer

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели привычки"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru',
            username='testuser',
            password='testpass123'
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=time(8, 0),
            action='Сделать зарядку',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

        self.assertEqual(habit.action, 'Сделать зарядку')
        self.assertEqual(habit.user.email, 'test@test.ru')
        self.assertEqual(habit.duration, 60)

    def test_habit_str_method(self):
        """Тест строкового представления"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=time(8, 0),
            action='Сделать зарядку',
            duration=60
        )
        expected = f"Сделать зарядку в 08:00:00 - test@test.ru"
        self.assertEqual(str(habit), expected)

    def test_periodicity_max_7(self):
        """Тест: периодичность не больше 7 дней"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time=time(8, 0),
            action='Сделать зарядку',
            periodicity=7,
            duration=60
        )
        habit.full_clean()
        habit.save()
        self.assertEqual(habit.periodicity, 7)

        habit2 = Habit(
            user=self.user,
            place='Дом',
            time=time(8, 0),
            action='Сделать зарядку',
            periodicity=8,
            duration=60
        )
        with self.assertRaises(Exception):
            habit2.full_clean()
            habit2.save()


class HabitAPITest(TestCase):
    """Тесты для API привычек"""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            email='user1@test.ru',
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.ru',
            username='user2',
            password='testpass123'
        )

        self.habit1 = Habit.objects.create(
            user=self.user1,
            place='Дом',
            time=time(8, 0),
            action='Зарядка',
            duration=60
        )
        self.habit2 = Habit.objects.create(
            user=self.user1,
            place='Офис',
            time=time(9, 0),
            action='Планерка',
            duration=30,
            is_public=True
        )
        self.habit3 = Habit.objects.create(
            user=self.user2,
            place='Спортзал',
            time=time(18, 0),
            action='Тренировка',
            duration=90
        )

    def test_get_habits_list_authenticated(self):
        """Тест: авторизованный пользователь видит только свои привычки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['action'], 'Планерка')
        self.assertEqual(response.data['results'][1]['action'], 'Зарядка')

    def test_get_habits_list_unauthenticated(self):
        """Тест: неавторизованный пользователь не видит привычки"""
        url = reverse('habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_authenticated(self):
        """Тест: создание привычки авторизованным пользователем"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habit-list')
        data = {
            'place': 'Парк',
            'time': '07:00:00',
            'action': 'Утренняя пробежка',
            'duration': 45,
            'periodicity': 1
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Утренняя пробежка')
        self.assertEqual(Habit.objects.count(), 4)

    def test_update_own_habit(self):
        """Тест: пользователь может обновить свою привычку"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habit-detail', args=[self.habit1.id])
        data = {'action': 'Зарядка обновленная'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, 'Зарядка обновленная')

    def test_update_other_user_habit(self):
        """Тест: пользователь не может обновить чужую привычку"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('habit-detail', args=[self.habit1.id])
        data = {'action': 'Попытка взлома'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_habit(self):
        """Тест: пользователь может удалить свою привычку"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habit-detail', args=[self.habit1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.filter(id=self.habit1.id).count(), 0)

    def test_delete_other_user_habit(self):
        """Тест: пользователь не может удалить чужую привычку"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('habit-detail', args=[self.habit1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Habit.objects.filter(id=self.habit1.id).count(), 1)

    def test_list_public_habits(self):
        """Тест: список публичных привычек"""
        url = reverse('habit-list-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['action'], 'Планерка')

    def test_pagination(self):
        """Тест: пагинация (по 5 привычек на страницу)"""
        for i in range(10):
            Habit.objects.create(
                user=self.user1,
                place=f'Место {i}',
                time=time(8, i),
                action=f'Действие {i}',
                duration=60
            )

        self.client.force_authenticate(user=self.user1)
        url = reverse('habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(len(response.data['results']), 5)


class HabitValidatorTest(TestCase):
    """Тесты для валидаторов привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru',
            username='test',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=time(12, 0),
            action='Приятная привычка',
            is_pleasant=True,
            duration=60
        )

    def test_related_habit_must_be_pleasant(self):
        """Тест: связанная привычка должна быть приятной"""
        unpleasant_habit = Habit.objects.create(
            user=self.user,
            place='Спортзал',
            time=time(18, 0),
            action='Неприятная',
            is_pleasant=False,
            duration=60
        )

        data = {
            'user': self.user.id,
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Полезная привычка',
            'related_habit': unpleasant_habit.id,
            'duration': 60
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Связанная привычка должна быть приятной', str(serializer.errors))

    def test_pleasant_habit_no_reward(self):
        """Тест: у приятной привычки не может быть вознаграждения"""
        data = {
            'user': self.user.id,
            'place': 'Дом',
            'time': '12:00:00',
            'action': 'Приятная привычка',
            'is_pleasant': True,
            'reward': 'Десерт',
            'duration': 60
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Приятная привычка не может иметь вознаграждение', str(serializer.errors))

    def test_cannot_both_reward_and_related(self):
        """Тест: нельзя одновременно указать вознаграждение и связанную привычку"""
        data = {
            'user': self.user.id,
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Полезная привычка',
            'reward': 'Конфета',
            'related_habit': self.pleasant_habit.id,
            'duration': 60
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
