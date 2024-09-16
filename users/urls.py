from django.urls import path

from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserProfileView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentViewSet, basename="payments")

urlpatterns = [
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user_profile"),
]

urlpatterns += router.urls
