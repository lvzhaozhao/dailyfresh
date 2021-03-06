# Generated by Django 2.2 on 2019-05-16 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_delete',
            field=models.BooleanField(default=True, verbose_name='删除标记'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='order_status',
            field=models.SmallIntegerField(choices=[(1, '待支付'), (2, '代发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1, verbose_name='订单状态'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='pay_method',
            field=models.SmallIntegerField(choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')], default=3, verbose_name='支付方式'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间'),
        ),
    ]
