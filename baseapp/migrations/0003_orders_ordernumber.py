# Generated by Django 3.2.5 on 2021-07-30 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='OrderNumber',
            field=models.IntegerField(null=True),
        ),
    ]
