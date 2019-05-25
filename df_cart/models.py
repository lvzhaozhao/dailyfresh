from django.db import models

# Create your models here.
from df_user.models import UserModel
from df_goods.models import GoodsModel


class CartModel(models.Model):
    """购物车"""
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, verbose_name="商品")
    count = models.IntegerField(default=1, verbose_name="商品数量")

    class Meta:
        db_table = "cart"
        verbose_name_plural = verbose_name = "购物车"
