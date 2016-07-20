from django.db import models
from embed_video.fields import EmbedVideoField
from multiselectfield import MultiSelectField
from datetime import datetime
import timedelta
from myapp.models import UserProfile
from django_social_app.models import MyUser



class Article(models.Model):

	MY_CHOICES = (('item_key1', 'Travel'),
              ('item_key2', 'Fitness'),
              ('item_key3', 'Music'),
              ('item_key4', 'Hobbies'),
              ('item_key5', 'Momentum')) 

	MY_SHARES = (('friends','FRIENDS'),('public','PUBLIC'))
	
	image = models.ImageField(upload_to="article_images/",blank=True)
	posted_by = models.CharField(max_length=255,default="Activork")
	video = EmbedVideoField(blank=True)
	latitude = models.FloatField(blank=True)
	longitude = models.FloatField(blank=True)
	approval_flag = models.BooleanField(default=True)
	share_with = models.CharField(max_length=20,choices=MY_SHARES,default="public")
	name = models.CharField(max_length=255,blank=True)
	time = models.DateTimeField(default=datetime.now(),blank=True)
	content = models.TextField(blank=True)
	interest = MultiSelectField(choices=MY_CHOICES,default='item_key1')
	sequence = models.IntegerField(default=0)
	tags=models.TextField(blank=True)

	def __unicode__(self):
		return self.name


class Comment(models.Model):
	article = models.ForeignKey(Article)
	comment = models.TextField(blank=True)
	commented_by = models.ForeignKey(UserProfile)


class Like(models.Model):
	article = models.ForeignKey(Article)
        #comment = models.TextField(blank=True)
        user = models.ForeignKey(UserProfile)
	like = models.BooleanField(default=False)
	rating = models.IntegerField(default=1)
	

class Follow_User(models.Model):
	follow = models.ForeignKey(UserProfile)
	followed_by = models.ForeignKey(UserProfile,related_name='followed_by')


class User_Stats(models.Model):
	#user = models.ForeignKey(User)
	article = models.ForeignKey(Article)
	start_time = models.DateTimeField(default=datetime.now(),blank=True)
	end_time = models.DateTimeField(default=datetime.now(),blank=True)
	time_duration = timedelta.fields.TimedeltaField()


class SimilarArticle(models.Model):
	article = models.ForeignKey(Article)
	selected = models.TextField(blank=True)

	def __unicode__(self):
		return self.article.name



