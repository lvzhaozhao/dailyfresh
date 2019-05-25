from django.db import models

# Create your models here.
from df_user.models import UserModel
from df_goods.models import GoodsModel


class OrderModel(models.Model):
    """订单管理模型"""
    PAY_METHOD = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )
    PAY_METHOD_DIC = {
        '1': '货到付款',
        '2': '微信支付',
        '3': '支付宝',
        '4': '银联支付'
    }
    ORDER_status = (
        (1, '待支付'),
        (2, '代发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成'),
    )
    ORDER_status_dic = {
        '1': '待支付',
        '2': '代发货',
        '3': '待收货',
        '4': '待评价',
        '5': '已完成',
    }
    # 订单的创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=True, verbose_name='删除标记')
    # 支付状态
    is_pay = models.BooleanField(verbose_name='是否支付', default=False)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD, default=3, verbose_name='支付方式')
    order_status = models.SmallIntegerField(choices=ORDER_status, default=1, verbose_name='订单状态')
    # 订单总价
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='总价')
    # 用户的外键关系
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, verbose_name='用户')

    class Meta:
        db_table = 'order'
        verbose_name_plural = verbose_name = '订单管理'

    def __str__(self):
        return str(self.id)


class OrderGoodsModel(models.Model):
    """订单和商品的关系"""
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name="订单")
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, verbose_name="商品")
    number = models.IntegerField(default=0, verbose_name="购买数量")

    class Meta:
        db_table = "order_goods"
        verbose_name_plural = verbose_name = "订单商品关系"
