# Generated by Django 4.0 on 2022-11-02 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_image_alter_product_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
