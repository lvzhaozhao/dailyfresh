from django.contrib import admin

from df_order.models import OrderModel
# Register your models here.


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price", "is_pay", "create_time")
