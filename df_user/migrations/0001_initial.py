# Generated by Django 2.1 on 2019-04-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('phone', models.CharField(max_length=11, verbose_name='电话号码')),
                ('address', models.CharField(blank=True, max_length=256, verbose_name='地址')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='电子邮箱')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user',
            },
        ),
    ]
