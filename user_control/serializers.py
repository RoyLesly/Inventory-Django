from rest_framework import serializers
from user_control.models import (CustomUser, ROLES, UserActivities)


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.ChoiceField(ROLES)


class LoginSerialiser(serializers.Serializer):
    first_name = serializers.CharField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False, required=False)


class UpdatePasswordUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.Serializer):

    class Meta:
        model = CustomUser
        exclude = ("password", "photo",)


class UserActivitiesSerializer(serializers.Serializer):

    class Meta:
        model = UserActivities
        fields = ("__all__")
