from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'units')  # Отображаемые поля в списке
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # Фильтры по полю
    search_fields = ('email', 'username')  # Поля для поиска

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'units')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
