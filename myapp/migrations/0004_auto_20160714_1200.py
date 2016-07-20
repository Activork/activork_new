# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20160713_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimilarEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.TextField(blank=True)),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='event_promotion',
            name='event',
        ),
        migrations.DeleteModel(
            name='Event_Promotion',
        ),
        migrations.RemoveField(
            model_name='hangout_imagegallery',
            name='hangout',
        ),
        migrations.RemoveField(
            model_name='hangout_imagegallery',
            name='uploaded_by',
        ),
        migrations.DeleteModel(
            name='Hangout_ImageGallery',
        ),
        migrations.RemoveField(
            model_name='hangout_liked',
            name='hangout',
        ),
        migrations.RemoveField(
            model_name='hangout_liked',
            name='user',
        ),
        migrations.DeleteModel(
            name='Hangout_Liked',
        ),
        migrations.RemoveField(
            model_name='hangout_promotion',
            name='hangout',
        ),
        migrations.DeleteModel(
            name='Hangout_Promotion',
        ),
        migrations.RemoveField(
            model_name='hangout_staff',
            name='hangout',
        ),
        migrations.DeleteModel(
            name='Hangout_Staff',
        ),
        migrations.RemoveField(
            model_name='hangoutpermission',
            name='access',
        ),
        migrations.RemoveField(
            model_name='hangoutpermission',
            name='hangout',
        ),
        migrations.DeleteModel(
            name='HangoutPermission',
        ),
        migrations.RemoveField(
            model_name='hangout',
            name='owner',
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.TextField(default=2, blank=True),
            preserve_default=False,
        ),
    ]
