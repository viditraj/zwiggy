# Generated by Django 4.1.4 on 2023-02-08 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_fooditem_is_veg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fooditem',
            old_name='is_veg',
            new_name='is_non_veg',
        ),
    ]
