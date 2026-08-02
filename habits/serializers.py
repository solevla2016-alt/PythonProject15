from rest_framework import serializers
from .models import Habit
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)  # Пользователь устанавливается автоматически

    def validate(self, data):
        """Кастомная валидация для DRF"""
        reward = data.get("reward")
        associated_habit = data.get("associated_habit")
        is_pleasant = data.get("is_pleasant", False)
        execution_time = data.get("execution_time")
        periodicity = data.get("periodicity", 1)

        # 1. Нельзя одновременно указывать вознаграждение и связанную привычку
        if reward and associated_habit:
            raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

        # 2. Время выполнения не больше 120 секунд
        if execution_time and execution_time > 120:
            raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд.")

        # 3. В связанные привычки могут попадать только приятные привычки
        if associated_habit and not associated_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна иметь признак 'приятная'.")

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if is_pleasant and (reward or associated_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # 5. Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        if periodicity > 7:
            raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=make_password(validated_data["password"]),
        )
        return user
