# Generated by Django 2.0.2 on 2018-02-07 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0009_auto_20180206_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopinfo',
            name='cropping',
        ),
        migrations.AlterField(
            model_name='shopinfo',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='shopinfo/icon', verbose_name='店铺图标'),
        ),
        migrations.AlterField(
            model_name='shopinfo',
            name='phone_num',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='联系电话'),
        ),
    ]