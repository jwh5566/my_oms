# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('installed', '0002_systeminstall_prifile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systeminstall',
            name='prifile',
        ),
        migrations.AddField(
            model_name='systeminstall',
            name='profile',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, verbose_name='profile\u6587\u4ef6\u540d'),
            preserve_default=False,
        ),
    ]
