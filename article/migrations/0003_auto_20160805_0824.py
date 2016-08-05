# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20160805_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='approval_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='share_with',
            field=models.CharField(default=b'friends', max_length=20, choices=[(b'friends', b'FRIENDS'), (b'public', b'PUBLIC')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 24, 34, 426976), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 24, 34, 430435), blank=True),
        ),
        migrations.AlterField(
            model_name='user_stats',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 24, 34, 430412), blank=True),
        ),
    ]
