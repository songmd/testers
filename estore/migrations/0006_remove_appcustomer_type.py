# Generated by Django 2.0.2 on 2018-02-20 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0005_auto_20180221_0243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appcustomer',
            name='type',
        ),
    ]
