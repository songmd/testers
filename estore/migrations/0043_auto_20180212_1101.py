# Generated by Django 2.0.2 on 2018-02-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0042_auto_20180212_0400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopinfo',
            name='feature',
        ),
        migrations.AddField(
            model_name='goods',
            name='pics',
            field=models.ManyToManyField(to='estore.Picture', verbose_name='图片'),
        ),
    ]
