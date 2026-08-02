from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Habit
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitSerializer
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer


class HabitPagination(LimitOffsetPagination):
    """Пагинация: 5 привычек на страницу"""

    default_limit = 5
    max_limit = 100


class HabitViewSet(viewsets.ModelViewSet):
    """
    CRUD для привычек текущего пользователя.
    GET /habits/my/ - список своих привычек
    POST /habits/my/ - создать привычку
    GET /habits/my/{id}/ - получить привычку
    PUT /habits/my/{id}/ - обновить привычку
    PATCH /habits/my/{id}/ - частично обновить привычку
    DELETE /habits/my/{id}/ - удалить привычку
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Возвращаем только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически устанавливаем пользователя при создании"""
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """
    Список публичных привычек (только чтение).
    GET /habits/public/ - список публичных привычек
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Возвращаем только публичные привычки"""
        return Habit.objects.filter(is_public=True)


class UserRegistrationView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    POST /api/users/register/
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
