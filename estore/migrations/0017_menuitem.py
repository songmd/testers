# Generated by Django 2.0.2 on 2018-02-08 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0016_auto_20180208_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='caption')),
                ('url', models.CharField(blank=True, max_length=200, verbose_name='URL')),
                ('named_url', models.CharField(blank=True, max_length=200, verbose_name='named URL')),
                ('level', models.IntegerField(default=0, editable=False, verbose_name='level')),
                ('rank', models.IntegerField(default=0, editable=False, verbose_name='rank')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estore.MenuItem', verbose_name='parent')),
            ],
        ),
    ]
