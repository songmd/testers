# Generated by Django 2.0.2 on 2018-02-09 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0030_auto_20180209_0502'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='goodscategory',
            unique_together=set(),
        ),
    ]