# Generated by Django 3.2.5 on 2021-10-02 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0011_alter_customer_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='Address',
        ),
    ]