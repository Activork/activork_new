# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20160707_0704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event_liked',
            old_name='regular',
            new_name='going',
        ),
        migrations.AddField(
            model_name='event_liked',
            name='like',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
