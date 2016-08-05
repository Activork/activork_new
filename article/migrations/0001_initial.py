# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields
import datetime
import multiselectfield.db.fields
from django.conf import settings
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0006_auto_20160720_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'article_images/', blank=True)),
                ('video', embed_video.fields.EmbedVideoField(blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('approval_flag', models.BooleanField(default=True)),
                ('share_with', models.CharField(default=b'public', max_length=20, choices=[(b'friends', b'FRIENDS'), (b'public', b'PUBLIC')])),
                ('name', models.CharField(max_length=255, blank=True)),
                ('time', models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 8, 38, 752783), blank=True)),
                ('content', models.TextField(blank=True)),
                ('interest', multiselectfield.db.fields.MultiSelectField(default=b'item_key1', max_length=49, choices=[(b'item_key1', b'Travel'), (b'item_key2', b'Fitness'), (b'item_key3', b'Music'), (b'item_key4', b'Hobbies'), (b'item_key5', b'Momentum')])),
                ('sequence', models.IntegerField(default=0)),
                ('tags', models.TextField(blank=True)),
                ('posted_by', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('article', models.ForeignKey(to='article.Article')),
                ('commented_by', models.ForeignKey(to='myapp.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow', models.ForeignKey(to='myapp.UserProfile')),
                ('followed_by', models.ForeignKey(related_name=b'followed_by', to='myapp.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=1)),
                ('article', models.ForeignKey(to='article.Article')),
                ('user', models.ForeignKey(to='myapp.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimilarArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.TextField(blank=True)),
                ('article', models.ForeignKey(to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 8, 38, 756258), blank=True)),
                ('end_time', models.DateTimeField(default=datetime.datetime(2016, 8, 5, 8, 8, 38, 756287), blank=True)),
                ('time_duration', timedelta.fields.TimedeltaField()),
                ('article', models.ForeignKey(to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
