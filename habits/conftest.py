import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def another_user():
    return User.objects.create_user(username="anotheruser", password="testpass123")


@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        place="Дом",
        time="08:00:00",
        action="Делать зарядку",
        execution_time=60,
        periodicity=1,
        is_public=True,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
