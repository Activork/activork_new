# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields
import datetime
import multiselectfield.db.fields
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_user_details_user_details_earlier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'article_images/', blank=True)),
                ('posted_by', models.CharField(default=b'Activork', max_length=255)),
                ('video', embed_video.fields.EmbedVideoField(blank=True)),
                ('latitude', models.FloatField(blank=True)),
                ('longitude', models.FloatField(blank=True)),
                ('approval_flag', models.BooleanField(default=True)),
                ('share_with', models.CharField(default=b'public', max_length=20, choices=[(b'friends', b'FRIENDS'), (b'public', b'PUBLIC')])),
                ('name', models.CharField(max_length=255, blank=True)),
                ('time', models.DateTimeField(default=datetime.datetime(2016, 7, 16, 8, 53, 47, 578199), blank=True)),
                ('content', models.TextField(blank=True)),
                ('channels', multiselectfield.db.fields.MultiSelectField(default=b'item_key1', max_length=49, choices=[(b'item_key1', b'Travel'), (b'item_key2', b'Fitness'), (b'item_key3', b'Music'), (b'item_key4', b'Hobbies'), (b'item_key5', b'Momentum')])),
                ('sequence', models.IntegerField(default=0)),
                ('tags', models.TextField(blank=True)),
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
                ('article', models.ForeignKey(to='article.Article')),
                ('liked_by', models.ForeignKey(to='myapp.UserProfile')),
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
                ('start_time', models.DateTimeField(default=datetime.datetime(2016, 7, 16, 8, 53, 47, 581341), blank=True)),
                ('end_time', models.DateTimeField(default=datetime.datetime(2016, 7, 16, 8, 53, 47, 581371), blank=True)),
                ('time_duration', timedelta.fields.TimedeltaField()),
                ('article', models.ForeignKey(to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
