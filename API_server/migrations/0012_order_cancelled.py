# Generated by Django 3.2.3 on 2021-05-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_server', '0011_alter_order_delivery_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]