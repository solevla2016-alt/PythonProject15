import os

from celery import Celery
from celery.schedules import crontab

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создаем экземпляр Celery
app = Celery("config")

# Загружаем настройки из settings.py (все переменные с префиксом CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим задачи во всех установленных приложениях
app.autodiscover_tasks()

# Настройка расписания (Celery Beat)
app.conf.beat_schedule = {
    "send-habit-reminders": {
        "task": "habits.tasks.send_habit_reminders",
        "schedule": crontab(minute="*/1"),  # Каждую минуту (для тестирования)
        # 'schedule': crontab(hour='*/1', minute=0),  # Каждый час (для продакшена)
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
