from django.contrib import admin

from account.models import User, Profile
# Register your models here.


class ProfileInline(admin.TabularInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline
    ]


admin.site.register(User, UserAdmin)
