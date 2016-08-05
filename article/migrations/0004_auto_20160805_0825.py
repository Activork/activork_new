# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20160805_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 25, 55, 271258), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 25, 55, 274670), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 25, 55, 274641), blank=True),
        ),
    ]
