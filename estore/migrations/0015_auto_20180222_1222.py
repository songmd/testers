# Generated by Django 2.0.2 on 2018-02-22 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0014_auto_20180222_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='owner',
        ),
        migrations.AddField(
            model_name='appcustomer',
            name='basket',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer', to='estore.Basket', verbose_name='购物车'),
        ),
    ]
