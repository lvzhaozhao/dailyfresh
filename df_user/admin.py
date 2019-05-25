from django.contrib import admin
from df_user.models import UserModel, Address


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "email")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "receiver")
