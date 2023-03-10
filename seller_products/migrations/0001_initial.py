# Generated by Django 4.0.2 on 2022-10-18 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='seller_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sp_name', models.CharField(choices=[('potato', 'Potato'), ('tomato', 'Potato'), ('onion', 'Potato'), ('potato', 'Potato'), ('potato', 'Potato')], max_length=255)),
                ('sp_description', models.CharField(blank=True, max_length=255)),
                ('sp_validity', models.DateField()),
                ('sp_img', models.ImageField(upload_to='products_images')),
                ('sp_amount', models.DecimalField(decimal_places=2, max_digits=2)),
                ('sp_stock', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
