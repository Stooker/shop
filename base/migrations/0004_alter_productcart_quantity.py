# Generated by Django 4.1.7 on 2023-03-28 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_productcart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]