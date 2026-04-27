from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании автоматически подставляем пользователя"""
        serializer.save(user=self.request.user)


    @swagger_auto_schema(
        operation_description="Список публичных привычек",
        responses={200: HabitSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def list_public(self, request):
        """Список публичных привычек (доступны всем)"""
        public_habits = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)
