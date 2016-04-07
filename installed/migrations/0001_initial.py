# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstallRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('install_date', models.CharField(max_length=20, verbose_name='\u5b89\u88c5\u65f6\u95f4')),
                ('ip', models.CharField(max_length=20, verbose_name='\u5b89\u88c5IP')),
                ('system_version', models.CharField(max_length=20, verbose_name=b'\xe5\xae\x89\xe8\xa3\x85\xe6\x93\x8d\xe4\xbd\x9c\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac')),
            ],
            options={
                'verbose_name': '\u88c5\u673a\u8bb0\u5f55\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='SystemInstall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=20, verbose_name='\u5f85\u88c5\u673aIP')),
                ('hostname', models.CharField(max_length=30, verbose_name='\u4e3b\u673a\u540d')),
                ('macaddress', models.CharField(max_length=50, verbose_name='MAC\u5730\u5740')),
                ('system_version', models.CharField(max_length=20, verbose_name='\u64cd\u4f5c\u7cfb\u7edf')),
                ('install_date', models.DateTimeField(auto_now_add=True, verbose_name='\u5b89\u88c5\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u88c5\u673a\u5217\u8868',
                'verbose_name_plural': '\u88c5\u673a\u5217\u8868\u7ba1\u7406',
            },
        ),
    ]
