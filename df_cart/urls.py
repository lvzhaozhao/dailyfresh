from django.urls import path

from df_cart.views import cart, add, delete, update

app_name = "cart"

urlpatterns = [
    path("", cart, name="cart"),
    path("add/<goods_id>/<int:count>/", add, name="add"),
    path("delete/<cart_id>/", delete, name="delete"),
    path("updete/<int:cart_id>/<int:count>/", update, name="update"),
]
