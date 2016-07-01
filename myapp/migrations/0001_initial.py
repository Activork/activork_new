# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import multiselectfield.db.fields
from django.conf import settings
import image_cropping.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cover_pic', models.ImageField(upload_to=b'cover_pic')),
                ('name', models.TextField()),
                ('datetime', models.DateTimeField(blank=True)),
                ('about', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event_ImageGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gallery', models.ImageField(upload_to=b'image_gallery')),
                ('event', models.ForeignKey(to='myapp.Event')),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event_Liked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event_Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event_Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('designation', models.TextField()),
                ('phone', models.TextField(validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('days', models.CharField(max_length=12)),
                ('starttime', models.TimeField()),
                ('endtime', models.TimeField()),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hangout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cover_pic', models.ImageField(upload_to=b'cover_pic')),
                ('name', models.CharField(max_length=255)),
                ('weblink', models.CharField(max_length=255)),
                ('email', models.EmailField(unique=True, max_length=70, blank=True)),
                ('about', models.TextField()),
                ('address', models.TextField()),
                ('phone', models.TextField(validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hangout_ImageGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gallery', models.ImageField(upload_to=b'image_gallery')),
                ('hangout', models.ForeignKey(to='myapp.Hangout')),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hangout_Liked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('hangout', models.ForeignKey(to='myapp.Hangout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hangout_Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('hangout', models.ForeignKey(to='myapp.Hangout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hangout_Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('designation', models.TextField()),
                ('phone', models.TextField(validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('days', models.CharField(max_length=12)),
                ('starttime', models.TimeField()),
                ('endtime', models.TimeField()),
                ('hangout', models.ForeignKey(to='myapp.Hangout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HangoutPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('hangout', models.ForeignKey(to='myapp.Hangout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfileLimitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_of_profiles', models.IntegerField(default=20)),
                ('starttime', models.TimeField()),
                ('hangout', models.OneToOneField(to='myapp.Hangout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upload_Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', image_cropping.fields.ImageCropField(upload_to=b'profile_photos', blank=True)),
                (b'cropping', image_cropping.fields.ImageRatioField(b'image', '430x360', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interest_status', models.BooleanField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_image', models.ImageField(upload_to=b'profile_photos')),
                ('age', models.IntegerField(null=True)),
                ('designation', models.TextField()),
                ('channels', multiselectfield.db.fields.MultiSelectField(default=b'item_key1', max_length=49, choices=[(b'item_key1', b'Travel'), (b'item_key2', b'Fitness'), (b'item_key3', b'Music'), (b'item_key4', b'Hobbies'), (b'item_key5', b'Spiritual')])),
                ('credits', models.IntegerField(default=20)),
                ('regular', models.BooleanField(default=True)),
                ('working_at', models.TextField(default=b'', blank=True)),
                ('college', models.TextField(default=b'', blank=True)),
                ('about', models.TextField(default=b'', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.TextField()),
                ('user', models.ForeignKey(to='myapp.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user_connection',
            name='receiver',
            field=models.ForeignKey(related_name=b'receiver', to='myapp.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user_connection',
            name='sender',
            field=models.ForeignKey(to='myapp.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hangout_liked',
            name='user',
            field=models.ForeignKey(to='myapp.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event_liked',
            name='user',
            field=models.ForeignKey(to='myapp.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='hangout',
            field=models.ForeignKey(to='myapp.Hangout'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
