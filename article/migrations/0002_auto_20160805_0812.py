# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='article',
            name='longitude',
        ),
        migrations.AddField(
            model_name='article',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 12, 49, 685531), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 12, 49, 689110), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 12, 49, 689080), blank=True),
        ),
    ]
