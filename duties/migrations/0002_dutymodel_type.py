# Generated by Django 4.0.2 on 2022-10-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dutymodel',
            name='type',
            field=models.CharField(choices=[('customer', 'Customer '), ('internal', 'Internal  ')], default='customer', max_length=255),
            preserve_default=False,
        ),
    ]
