# Generated by Django 3.1.3 on 2020-12-15 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20201214_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='image',
            new_name='cover_image',
        ),
    ]