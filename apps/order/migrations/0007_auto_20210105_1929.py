# Generated by Django 3.1.3 on 2021-01-05 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210105_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 12, 19, 29, 4, 259461)),
        ),
    ]