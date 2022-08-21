from ast import Mod
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CreateUserSerializer, CustomUser, CustomUserSerializer,
    LoginSerialiser, UpdatePasswordUserSerializer, UserActivities, UserActivitiesSerializer
)
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import date, datetime
from inven_djan_api.utils import get_access_token, get_query, CustomPagination
from inven_djan_api.custom_methods import IsAuthenticatedCustom


def add_user_activity(user, action):
    UserActivities.objects.create(
        user_id=user.id,
        first_name=user.first_name,
        email=user.email,
        action=action
    )


class CreateUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def create(self, request):
        print(request.data)
        valid_request = self.serializer_class(data=request.data)

        try:
            valid_request.is_valid(raise_exception=True)
            if CustomUser.objects.filter(first_name=request.data["first_name"]):
                return Response(
                    {"error": "First Name Exist Already"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif CustomUser.objects.filter(email=request.data["email"]):
                return Response(
                    {"error": "Email Exist Already"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            print("invalid")
            print(valid_request.errors)
            return Response(
                {"error": "Invalid Email"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            CustomUser.objects.create(**valid_request.validated_data)
        except:
            return Response(
                {"error": "Server Error"},
                status=status.HTTP_400_BAD_REQUEST
            )

        add_user_activity(request.user, "added new user")

        return Response(
            {"success": "User Created Successfully"},
            status=status.HTTP_201_CREATED
        )


class LoginView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerialiser

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)

        new_user = valid_request.validated_data["is_new_user"]

        if new_user:
            user = CustomUser.objects.filter(
                first_name=valid_request.validated_data["first_name"]
            )
            if user:
                user = user[0]
                if not user.password:
                    return Response({"user_id": user.id})
                else:
                    raise Exception("User has Password Already")
            else:
                raise Exception("User With First Name not Found")
        user = authenticate(
            first_name=valid_request.validated_data["first_name"],
            password=valid_request.validated_data.get("password", None)
        )
        print(valid_request.validated_data["first_name"])
        if not user:
            return Response(
                {"error": "Invalid First Name or Password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        access = get_access_token({"user_id": user.id}, 1)

        print("here")
        print(user)
        print(user.id)
        print(user.first_name)
        print(user.role)
        user.last_login = datetime.now()
        user.save()

        add_user_activity(user, "logged in")

        return Response({"access": access, "user_name": user.first_name, "user_role": user.role})


class UpdatePasswordView(ModelViewSet):
    serializer_class = UpdatePasswordUserSerializer
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()

    def create(self, request):
        print(request.data)
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        print("here")

        user = CustomUser.objects.filter(
            id=valid_request.validated_data["user_id"])

        if not user:
            raise Exception("User with Id not Found")

        user = user[0]

        user.set_password(valid_request.validated_data["password"])
        user.save()

        add_user_activity(user, "updated password")

        return Response({"success": "User Password Updated"})


class MeView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )

    def list(self, request):
        #data1 = self.serializer_class(request.user).data
        data1 = CustomUser.objects.get(id=request.user.id)
        user = {
            "id": data1.id,
            "first_name": data1.first_name,
            "last_login": data1.last_login,
            "created_at": data1.created_at,
            "role": data1.role,
            "email": data1.email,
        }
        print(user)

        return Response(user)


class UserActivitiesView(ModelViewSet):
    serializer_class = UserActivitiesSerializer
    http_method_names = ["get"]
    queryset = UserActivities.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    class Meta:
        ordering = ("-created_at", )

    def list(self, request):
        userActivities = self.queryset  # .filter(is_superuser=False)
        #data = self.serializer_class(users, many=True).data

        list_users = []
        for user in userActivities:
            u = {
                "id": user.id,
                "first_name": user.first_name,
                "email": user.email,
                "actions": user.action,
                "created_at": user.created_at,
            }
            list_users.append(u)

        return Response(list_users)


class UsersView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )

    def list(self, request):
        users = self.queryset.filter(is_superuser=False)
        #data = self.serializer_class(users, many=True).data

        list_users = []
        for user in users:
            u = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "last_login": user.last_login,
                "created_at": user.created_at,
                "role": user.role,
                "email": user.email,
                "is_active": user.is_active,
            }
            list_users.append(u)
        print(list_users)

        return Response(list_users)
