from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits", verbose_name="Пользователь")
    place = models.CharField(max_length=255, blank=True, null=True, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parent_habits",
        verbose_name="Связанная привычка",
    )

    periodicity = models.IntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.IntegerField(verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def clean(self):
        # 1. Исключить одновременный выбор связанной привычки и вознаграждения
        if self.reward and self.associated_habit:
            raise ValidationError(
                {
                    "reward": "Нельзя одновременно указывать вознаграждение и связанную привычку.",
                    "associated_habit": "Нельзя одновременно указывать вознаграждение и связанную привычку.",
                }
            )

        # 2. Время выполнения должно быть не больше 120 секунд
        if self.execution_time > 120:
            raise ValidationError({"execution_time": "Время выполнения должно быть не больше 120 секунд."})

        # 3. В связанные привычки могут попадать только привычки с признаком приятной привычки
        if self.associated_habit and not self.associated_habit.is_pleasant:
            raise ValidationError({"associated_habit": 'Связанная привычка должна иметь признак "приятная".'})

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.associated_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        # 5. Нельзя выполнять привычку реже, чем 1 раз в 7 дней (периодичность <= 7)
        if self.periodicity > 7:
            raise ValidationError({"periodicity": "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."})

    def __str__(self):
        return f"Привычка: {self.action} ({self.user.username})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-id"]
