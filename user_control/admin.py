from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import UserActivities


class CustomUserAdminConfig(UserAdmin):
    model = CustomUser
    list_display = ('username', 'id', 'role', 'last_login', 'email',
                    'is_active', 'is_staff', 'is_superuser', 'is_admin')
    search_fields = ('username', 'role')
    list_filter = ('username', 'role', 'is_active', 'is_staff', 'is_superuser', 'is_admin')
    ordering = ('id',)
    exclude = ('email', 'last_name', 'date_joined', 'first_name', )

#admin.site.register(CustomUser, CustomUserAdminConfig)
admin.site.register((CustomUser, UserActivities))
