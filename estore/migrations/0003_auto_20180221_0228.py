# Generated by Django 2.0.2 on 2018-02-20 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0002_auto_20180221_0050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appcustomer',
            old_name='nick_name',
            new_name='user_info',
        ),
    ]
