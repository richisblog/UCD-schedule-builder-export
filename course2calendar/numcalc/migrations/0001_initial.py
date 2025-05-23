# Generated by Django 5.2.1 on 2025-05-20 12:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_number', models.FloatField(verbose_name='第一个数字')),
                ('second_number', models.FloatField(verbose_name='第二个数字')),
                ('result', models.FloatField(verbose_name='计算结果')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '计算',
                'verbose_name_plural': '计算',
                'ordering': ['-created_at'],
            },
        ),
    ]
