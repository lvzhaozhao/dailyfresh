from django.urls import path


from df_goods.views import goods_list, detail, search_detail

app_name = "goods"
urlpatterns = [
    path("list/<category_id>/<sort>/<page_num>", goods_list, name="list"),
    path("detail/<goods_id>/", detail, name="detail"),
    path("search_detail/", search_detail, name="search_detail")
]
