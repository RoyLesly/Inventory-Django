from django.urls import path, include
from rest_framework import routers
from user_control.models import UserActivities
from user_control.views import (
    CreateUserView, LoginView, UpdatePasswordView, MeView, UserActivitiesView, UsersView,
    UserActivitiesView, UsersView
)

app_name = "user_control"

router = routers.DefaultRouter(trailing_slash=False)
router.register("create-user", CreateUserView, "create user")
router.register("login", LoginView, "login")
router.register("update-password", UpdatePasswordView, "update password")
router.register("me", MeView, "me")
router.register("activities-log", UserActivitiesView, "activities log")
router.register("users", UsersView, "users")

urlpatterns = [
    path('/', include(router.urls)),
]
