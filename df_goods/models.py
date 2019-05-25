from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class CategoryModel(models.Model):
    """商品的分类"""
    category_name = models.CharField(max_length=20, null=False, verbose_name="商品分类名称")
    # 分类的图片
    image = models.ImageField(upload_to="category/", blank=True)

    class Meta:
        db_table = "category"
        verbose_name_plural = verbose_name = "商品分类"

    def __str__(self):
        return self.category_name


class GoodsModel(models.Model):
    """商品模型"""
    goods_name = models.CharField(max_length=50, null=False, verbose_name="商品名称")
    abstract = models.CharField(max_length=200, null=False, verbose_name="商品简介")
    # max_digits 总共限制几位，decimal_places 小数点后的几位
    price = models.DecimalField(default=0, max_digits=11, decimal_places=2, verbose_name="商品价格")
    unit = models.CharField(max_length=20, null=False, verbose_name="商品的售卖单位")
    stock = models.IntegerField(default=0, verbose_name="商品库存")
    desc = RichTextUploadingField(null=True, verbose_name="详细介绍")
    pic = models.ImageField(upload_to="goods/%Y/%m/%d", verbose_name="商品图片")
    category = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING, verbose_name="商品的分类")
    popular = models.IntegerField(default=0, verbose_name="人气指数")

    class Meta:
        db_table = "goods"
        verbose_name_plural = verbose_name = "商品表"

    def __str__(self):
        return self.goods_name
