# Generated by Django 4.1.7 on 2023-03-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcart',
            name='quantity',
            field=models.IntegerField(blank=True),
        ),
    ]
