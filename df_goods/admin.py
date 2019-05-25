from django.contrib import admin
from df_goods.models import CategoryModel, GoodsModel
# Register your models here.


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'image')


@admin.register(GoodsModel)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('goods_name',)
