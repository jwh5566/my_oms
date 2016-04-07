# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('installed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systeminstall',
            name='prifile',
            field=models.CharField(default=b'CentOS-6.6-mini-x86_64', max_length=50, verbose_name='profile\u6587\u4ef6\u540d'),
        ),
    ]
