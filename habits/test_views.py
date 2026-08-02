import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly


@pytest.mark.django_db
def test_public_habits_list(api_client, habit):
    """Тест: список публичных привычек доступен без авторизации"""
    url = reverse("habit-public")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_create_habit(authenticated_client, user):
    """Тест: авторизованный пользователь может создать привычку"""
    url = reverse("habit-my-list")
    data = {"place": "Офис", "time": "09:00:00", "action": "Пить воду", "execution_time": 30, "periodicity": 1}
    response = authenticated_client.post(url, data)
    assert response.status_code == 201
    assert Habit.objects.count() == 1
    assert Habit.objects.first().user == user


@pytest.mark.django_db
def test_cannot_delete_another_users_habit(authenticated_client, another_user, habit):
    """Тест: пользователь НЕ может удалить чужую привычку.
    Возвращается 404, так как объект отфильтровывается в get_queryset (безопасный подход)."""

    # Меняем владельца привычки на другого пользователя
    habit.user = another_user
    habit.save()

    url = reverse("habit-my-detail", kwargs={"pk": habit.pk})
    response = authenticated_client.delete(url)

    # DRF возвращает 404, потому что get_queryset фильтрует по текущему пользователю
    assert response.status_code == 404
    assert Habit.objects.count() == 1  # Привычка не удалена


@pytest.mark.django_db
def test_is_owner_or_readonly_permission(user, another_user, habit):
    """Тест прав доступа IsOwnerOrReadOnly напрямую"""
    permission = IsOwnerOrReadOnly()
    factory = APIRequestFactory()

    # 1. Тест на чтение (GET) - должно быть разрешено всем (даже чужим пользователям)
    request = factory.get("/")
    request.user = another_user
    assert permission.has_object_permission(request, None, habit) is True

    # 2. Тест на удаление (DELETE) для владельца - разрешено
    request = factory.delete("/")
    request.user = user
    assert permission.has_object_permission(request, None, habit) is True

    # 3. Тест на удаление (DELETE) для чужого пользователя - запрещено
    request = factory.delete("/")
    request.user = another_user
    assert permission.has_object_permission(request, None, habit) is False
