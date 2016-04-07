# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostlist',
            name='status',
            field=models.CharField(default='\u5f85\u88c5\u673a', max_length=10, verbose_name='\u4f7f\u7528\u72b6\u6001'),
        ),
    ]
