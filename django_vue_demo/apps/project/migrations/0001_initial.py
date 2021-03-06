# Generated by Django 3.1.3 on 2021-05-13 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('prj_id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目id')),
                ('prj_name', models.CharField(max_length=50, verbose_name='项目名称')),
                ('version', models.CharField(max_length=20, verbose_name='项目版本')),
                ('description', models.CharField(max_length=100, verbose_name='项目描述')),
                ('status', models.SmallIntegerField(choices=[(1, '有效'), (0, '失效')], default=1, verbose_name='项目状态')),
            ],
        ),
    ]
