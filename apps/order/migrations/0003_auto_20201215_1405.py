# Generated by Django 3.1.3 on 2020-12-15 14:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201214_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 22, 14, 5, 26, 16160)),
        ),
    ]
