# Generated by Django 2.0.2 on 2018-02-22 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0016_auto_20180222_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcustomer',
            name='basket',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer', to='estore.Basket', verbose_name='购物车'),
        ),
        migrations.AlterField(
            model_name='basketlineunit',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='estore.Product', verbose_name='商品'),
        ),
    ]