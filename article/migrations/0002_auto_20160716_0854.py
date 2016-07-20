# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 16, 8, 54, 22, 486261), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 16, 8, 54, 22, 489444), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 16, 8, 54, 22, 489418), blank=True),
        ),
    ]
