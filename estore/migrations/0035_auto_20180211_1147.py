# Generated by Django 2.0.2 on 2018-02-11 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0034_auto_20180211_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodspictures',
            old_name='icon',
            new_name='picture',
        ),
    ]
