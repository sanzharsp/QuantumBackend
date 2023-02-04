from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UsersAdmin(UserAdmin):
    model = User
    list_display = ('username', 'is_superuser', 'is_staff')
    list_filter = ('username', 'is_superuser', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'surname', 'email',)}),
        ('Права доступа и потверждение', {'fields': ('is_staff', 'is_superuser')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'surname', 'email',)},

         ),
        ('Права доступа и потверждение', {'fields': ('is_staff', 'is_superuser')}),
    )
    search_fields = ('username',)
    ordering = ('username',)


class JKAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class ProfileAdminAdmin(admin.ModelAdmin):
    list_display = ('user','JK','room_number')
    search_fields = ('user','room_number',)
    ordering = ('user','room_number',)


class QrCodeAdminAdmin(admin.ModelAdmin):
    list_display = ('user','id_in_electron',)
    search_fields = ('user','id_in_electron',)
    ordering = ('user','id_in_electron',)
    
admin.site.register(User, UsersAdmin)
admin.site.register(JK, JKAdmin)
admin.site.register(Profile, ProfileAdminAdmin)
admin.site.register(QrCode, QrCodeAdminAdmin)

