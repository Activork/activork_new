# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20160716_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='channels',
            new_name='interest',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='liked_by',
            new_name='user',
        ),
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 20, 7, 27, 39, 613355), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 20, 7, 27, 39, 616581), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 20, 7, 27, 39, 616555), blank=True),
        ),
    ]
