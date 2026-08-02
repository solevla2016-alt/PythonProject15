from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register(r"my", HabitViewSet, basename="habit-my")

urlpatterns = [
    path("", include(router.urls)),
    path("public/", PublicHabitListView.as_view(), name="habit-public"),
]
