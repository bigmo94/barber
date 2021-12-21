from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from customers.models import Store, Employee

User = get_user_model()


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_id', 'phone', 'address', 'store_type', 'is_active']
    filter_horizontal = ['service']
    readonly_fields = ['client_id']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'is_enable']
    filter_horizontal = ['service']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'birthday', 'email',
                    'phone', 'gender', 'avatar', 'is_enable']
    readonly_fields = ['password']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'birthday', 'gender', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_enable', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
