from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'firstname',)
    list_filter = ('email', 'username', 'firstname', 'is_active',
                   'is_staff', 'is_superuser', 'Joined_date', 'Mail_opt_in')
    ordering = ('-Joined_date',)
    list_display = ('id', 'email', 'username', 'firstname',
                    'is_active', 'is_superuser', 'Joined_date', 'is_staff', 'Mail_opt_in')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'firstname', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'Mail_opt_in')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','firstname', 'password1', 'is_staff', 'password2', 'is_active', 'is_superuser', 'Mail_opt_in')}
         ),
    )
