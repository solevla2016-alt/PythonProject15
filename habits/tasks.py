from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings

from habits.models import Habit


@shared_task
def send_habit_reminders():
    print("=" * 60)
    print(" ЗАПУСК ЗАДАЧИ send_habit_reminders")

    # Получаем настройки
    bot_token = getattr(settings, "TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "").strip()

    print(f" Токен: {'НАЙДЕН' if bot_token else 'ОТСУТСТВУЕТ (пустая строка)'}")
    print(f" Chat ID: {chat_id if chat_id else 'ОТСУТСТВУЕТ (пустая строка)'}")

    if not bot_token or not chat_id:
        print("ОШИБКА: TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID пусты в настройках Django!")
        print(" Проверь файл .env и перезапусти Celery.")
        print("=" * 60)
        return "No credentials"

    # Текущее время без секунд
    current_time = datetime.now().time().replace(second=0, microsecond=0)
    print(f"Ищем привычки на время: {current_time}")

    # Ищем привычки
    habits_to_remind = Habit.objects.filter(time=current_time)
    print(f"Найдено привычек в базе для этого времени: {habits_to_remind.count()}")

    sent_count = 0
    for habit in habits_to_remind:
        message = (
            f" Напоминание о привычке!\n"
            f"Действие: {habit.action}\n"
            f" Место: {habit.place or 'Не указано'}\n"
            f"⏱На выполнение: {habit.execution_time} сек."
        )
        if habit.reward:
            message += f"\n Вознаграждение: {habit.reward}"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": str(chat_id), "text": message, "parse_mode": "HTML"}  # Гарантируем строку

        print(" Пытаемся отправить в Telegram...")
        # Скрываем токен в логе для безопасности
        safe_url = url.replace(bot_token, "***СКРЫТО***")
        print(f"   URL: {safe_url}")
        print(f"   Payload: {payload}")

        try:
            response = requests.post(url, json=payload, timeout=5)
            print(f"   Статус ответа: {response.status_code}")
            print(f"   Текст ответа: {response.text}")

            if response.status_code == 200:
                sent_count += 1
                print("Успешно отправлено!")
            else:
                print("Ошибка API Telegram (см. текст ответа выше)")
        except requests.exceptions.RequestException as e:
            print(f" Ошибка сети: {e}")

    print(f"ИТОГО: Успешно отправлено {sent_count} напоминаний.")
    print("=" * 60)
    return f"Sent {sent_count} reminders"
