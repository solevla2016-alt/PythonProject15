import pytest
from django.core.exceptions import ValidationError

from habits.models import Habit


@pytest.mark.django_db
def test_habit_creation(habit):
    """Тест успешного создания привычки"""
    assert habit.action == "Делать зарядку"
    assert habit.execution_time == 60


@pytest.mark.django_db
def test_execution_time_validator(user):
    """Тест: время выполнения не больше 120 секунд"""
    habit = Habit(user=user, time="08:00:00", action="Тест", execution_time=150, periodicity=1)
    with pytest.raises(ValidationError) as excinfo:
        habit.full_clean()
    assert "Время выполнения должно быть не больше 120 секунд" in str(excinfo.value)


@pytest.mark.django_db
def test_periodicity_validator(user):
    """Тест: нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    habit = Habit(user=user, time="08:00:00", action="Тест", execution_time=60, periodicity=10)
    with pytest.raises(ValidationError) as excinfo:
        habit.full_clean()
    assert "реже, чем 1 раз в 7 дней" in str(excinfo.value)


@pytest.mark.django_db
def test_pleasant_habit_restrictions(user):
    """Тест: у приятной привычки не может быть вознаграждения"""
    pleasant_habit = Habit.objects.create(
        user=user, time="08:00:00", action="Отдых", is_pleasant=True, execution_time=60
    )
    main_habit = Habit(
        user=user,
        time="09:00:00",
        action="Работа",
        execution_time=60,
        periodicity=1,
        reward="Шоколадка",
        associated_habit=pleasant_habit,
    )
    with pytest.raises(ValidationError):
        main_habit.full_clean()
