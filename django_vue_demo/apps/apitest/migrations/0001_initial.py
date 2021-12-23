# Generated by Django 3.1.3 on 2021-05-13 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_id', models.AutoField(primary_key=True, serialize=False, verbose_name='用例ID')),
                ('case_name', models.CharField(max_length=50, verbose_name='用例名称')),
                ('description', models.CharField(max_length=50, verbose_name='用例描述')),
                ('content', models.TextField(verbose_name='用例内容')),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('if_id', models.AutoField(primary_key=True, serialize=False, verbose_name='接口id')),
                ('if_name', models.CharField(max_length=50, verbose_name='接口名称')),
                ('if_url', models.CharField(max_length=50, verbose_name='接口地址')),
                ('method', models.CharField(max_length=4, verbose_name='接口请求方法')),
                ('data_type', models.CharField(max_length=4, verbose_name='接口请求头类型')),
                ('description', models.CharField(max_length=50, verbose_name='接口描述')),
                ('request_header_param', models.TextField(verbose_name='请求头')),
                ('request_body_param', models.TextField(verbose_name='请求体')),
                ('response_header_param', models.TextField(verbose_name='响应头')),
                ('response_body_param', models.TextField(verbose_name='响应体')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('plant_id', models.AutoField(primary_key=True, serialize=False, verbose_name='计划id')),
                ('plant_name', models.CharField(max_length=50, verbose_name='计划名称')),
                ('description', models.CharField(max_length=50, verbose_name='计划描述')),
                ('content', models.TextField(verbose_name='计划内容')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False, verbose_name='报告ID')),
                ('report_name', models.CharField(max_length=50, verbose_name='报告名称')),
                ('content', models.TextField(verbose_name='报告内容')),
                ('case_num', models.IntegerField(null=True, verbose_name='用例数量')),
                ('pass_num', models.IntegerField(null=True, verbose_name='通过数量')),
                ('fail_num', models.IntegerField(null=True, verbose_name='失败数量')),
                ('error_num', models.IntegerField(null=True, verbose_name='错误数量')),
                ('plant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.plan', verbose_name='报告对应的计划')),
            ],
        ),
    ]