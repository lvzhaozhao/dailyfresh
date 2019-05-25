from django.urls import path

from df_order.views import order, add_order, order_main

app_name = "order"
urlpatterns = [
    path("order/<good_id>/", order, name="order"),
    path("order/", order_main, name="order"),
    path("add_order/", add_order, name="add_order"),
]
