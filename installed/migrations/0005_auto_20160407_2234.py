# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('installed', '0004_auto_20160407_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installrecord',
            name='system_version',
            field=models.CharField(max_length=50, verbose_name=b'\xe5\xae\x89\xe8\xa3\x85\xe6\x93\x8d\xe4\xbd\x9c\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac'),
        ),
    ]
