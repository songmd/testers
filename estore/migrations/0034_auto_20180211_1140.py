# Generated by Django 2.0.2 on 2018-02-11 11:40

from django.db import migrations, models
import django.db.models.deletion
import estore.imagefieldex


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0033_auto_20180211_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsPictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', estore.imagefieldex.ImageFieldEx(blank=True, null=True, upload_to='estorepics/goods', verbose_name='店铺图标')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '选择图片',
            },
        ),
        migrations.RemoveField(
            model_name='goods',
            name='pics',
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='estorepics', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='shopinfo',
            name='icon',
            field=estore.imagefieldex.ImageFieldEx(blank=True, null=True, upload_to='shopinfo/icon', verbose_name='店铺图标'),
        ),
        migrations.AddField(
            model_name='goodspictures',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='estore.Goods'),
        ),
    ]
