# Generated by Django 2.0.2 on 2018-02-12 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0040_auto_20180212_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopinfo',
            name='icon',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estore.Picture', verbose_name='店铺图标'),
        ),
    ]
