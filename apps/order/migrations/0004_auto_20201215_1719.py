# Generated by Django 3.1.3 on 2020-12-15 17:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20201215_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 22, 17, 19, 9, 569042)),
        ),
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.coupon'),
        ),
    ]