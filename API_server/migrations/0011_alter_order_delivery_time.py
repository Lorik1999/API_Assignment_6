# Generated by Django 3.2.3 on 2021-05-27 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_server', '0010_alter_order_pizzas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(),
        ),
    ]