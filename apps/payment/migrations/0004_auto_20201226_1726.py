# Generated by Django 3.1.3 on 2020-12-26 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20201223_0634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='zipcode',
        ),
    ]
