from operator import mod
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


ROLES = (
    ("zane", "zane"), ("admin", "admin"), ("creator", "creator"), ("sale", "sale"),
    ("user1", "user1"), ("user2", "user2"), ("user3", "user3"), ("user4", "user4"),
    ("user5", "user5"), ("user6", "user6"), ("user7", "user7"),
)


class CustomUserManager(BaseUserManager):

    # def create_user(self, password, first_name, last_name, email, **extra_fields):
    #     print("Creating User .........................")
    #     print(extra_fields)

    #     if not username:
    #         raise ValueError("Username Field Is Required")

    #     user = self.model(
    #         username=username,
    #         email=email, full_name=full_name,
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)

    #     return user

    def create_superuser(self, password, first_name, last_name, email, **extra_fields):
        print("CREATING SUPER USER ................................")
        print(extra_fields)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser Must Have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser Must Have is_superuser=True")

        if not first_name:
            raise ValueError("First Name Field Is Required")

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields, 
        )
        user.set_password(password)
        user.save()
        # user.role = extra_fields["role"]
        # user.is_staff = True
        # user.is_staff = True
        # user.is_admin = True
        # user.is_superuser = True
        # user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True, verbose_name='email')
    role = models.CharField(max_length=15, choices=ROLES, blank=False)
    # password = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "first_name"
    REQUIRED_FIELDS = ["role", "last_name", 'email']
    objects = CustomUserManager()

    def __str__(self):
        return (self.first_name + " " + self.last_name)

    class Meta:
        ordering = ("created_at",)


class UserActivities(models.Model):
    user = models.ForeignKey( CustomUser, related_name="user_activities", null=True, on_delete=models.SET_NULL )
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        #return f"{self.first_name} {self.action} on {self.created_at('%Y-%m-%d %H:%M')}"
        return f"{self.first_name} {self.action} on {self.created_at}"

