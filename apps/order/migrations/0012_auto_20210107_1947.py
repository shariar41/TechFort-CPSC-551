# Generated by Django 3.1.3 on 2021-01-07 19:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20201215_1407'),
        ('order', '0011_auto_20210107_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 14, 19, 47, 58, 160072)),
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]