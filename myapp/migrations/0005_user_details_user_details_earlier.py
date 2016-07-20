# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0004_auto_20160714_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(blank=True)),
                ('interest', multiselectfield.db.fields.MultiSelectField(default=b'item_key1', max_length=49, choices=[(b'item_key1', b'Travel'), (b'item_key2', b'Fitness'), (b'item_key3', b'Music'), (b'item_key4', b'Hobbies'), (b'item_key5', b'Momentum')])),
                ('latitude', models.FloatField(blank=True)),
                ('longitude', models.FloatField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Details_Earlier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(unique=True)),
                ('latitude', models.FloatField(blank=True)),
                ('longitude', models.FloatField(blank=True)),
                ('interest', multiselectfield.db.fields.MultiSelectField(default=b'item_key1', max_length=49, choices=[(b'item_key1', b'Travel'), (b'item_key2', b'Fitness'), (b'item_key3', b'Music'), (b'item_key4', b'Hobbies'), (b'item_key5', b'Momentum')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
