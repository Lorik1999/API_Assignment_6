# Generated by Django 3.2.3 on 2021-05-24 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_server', '0004_pizza_pizza_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
