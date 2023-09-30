from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import VoteUser, School, Question, Vote, Choice

class VoteUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'school', 'is_staff',
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'school')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'school')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

# Register your models here.
admin.site.register(VoteUser, VoteUserAdmin)
admin.site.register(School)
admin.site.register(Question)
admin.site.register(Vote)
admin.site.register(Choice)