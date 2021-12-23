# Generated by Django 3.1.3 on 2021-05-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taste_user', '0003_auto_20210513_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taste',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'STOP'), (1, 'RUNNING'), (3, 'RESUME'), (2, 'PAUSE')], default=0, verbose_name='任务状态'),
        ),
    ]
