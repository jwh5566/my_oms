# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=20, verbose_name='IP\u5730\u5740')),
                ('hostname', models.CharField(max_length=30, verbose_name='\u4e3b\u673a\u540d')),
                ('product', models.CharField(max_length=20, verbose_name='\u4ea7\u54c1')),
                ('application', models.CharField(max_length=20, verbose_name='\u5e94\u7528')),
                ('idc_jg', models.CharField(max_length=10, verbose_name='\u673a\u67dc\u7f16\u53f7', blank=True)),
                ('status', models.CharField(max_length=10, verbose_name='\u4f7f\u7528\u72b6\u6001')),
                ('remark', models.TextField(max_length=50, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u5217\u8868\u7ba1\u7406',
            },
        ),
    ]
