# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('installed', '0003_auto_20160407_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installrecord',
            name='install_date',
            field=models.CharField(max_length=50, verbose_name='\u5b89\u88c5\u65f6\u95f4'),
        ),
    ]
