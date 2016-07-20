# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_user_details_user_details_earlier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('commented_by', models.ForeignKey(to='myapp.UserProfile')),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='interest',
            field=multiselectfield.db.fields.MultiSelectField(default=b'item_key1', max_length=49, choices=[(b'item_key1', b'Travel'), (b'item_key2', b'Fitness'), (b'item_key3', b'Music'), (b'item_key4', b'Hobbies'), (b'item_key5', b'Momentum')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event_liked',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userstatus',
            name='public',
            field=models.BooleanField(default=0),
            preserve_default=True,
        ),
    ]
