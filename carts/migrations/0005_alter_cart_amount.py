# Generated by Django 4.0.2 on 2022-10-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
