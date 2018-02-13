# Generated by Django 2.0.2 on 2018-02-09 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('estore', '0029_auto_20180209_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodscategorywrap',
            name='category',
        ),
        migrations.RemoveField(
            model_name='goodscategorywrap',
            name='owner',
        ),
        migrations.AddField(
            model_name='goodscategory',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='商户'),
        ),
        migrations.AlterUniqueTogether(
            name='goodscategory',
            unique_together={('owner', 'name')},
        ),
        migrations.DeleteModel(
            name='GoodsCategoryWrap',
        ),
    ]
