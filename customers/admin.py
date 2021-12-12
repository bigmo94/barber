from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'birthday', 'email',
                    'phone', 'gender', 'avatar', 'is_active']
    readonly_fields = ['get_access', 'password']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'get_access')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'birthday', 'gender', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
