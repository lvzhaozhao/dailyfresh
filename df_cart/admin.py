from django.contrib import admin

from df_cart.models import CartModel
# Register your models here.


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ("goods", "count", "user")
