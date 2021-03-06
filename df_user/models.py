from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    """用户数据模型"""
    # 密码
    password = models.CharField(max_length=250, null=False, verbose_name="密码")
    # 电子邮箱
    email = models.EmailField(null=False, verbose_name="电子邮箱", blank=True)

    class Meta:
        verbose_name_plural = verbose_name = "用户"
        db_table = "user"

    def __str__(self):
        return self.username


class AddressManager(models.Manager):
    '''地址模型管理器类'''
    # 1.改变原有查询的结果集:all()
    # 2.封装方法：用户操作模型类对应的数据表(增删改查)
    def get_default_address(self, user):
        '''获取用户默认收货地址'''
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # 没有默认地址
            address = None
        return address


class Address(models.Model):
    '''地址模型类'''
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='所属账户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义一个模型管理器对象
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name
