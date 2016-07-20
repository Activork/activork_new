from myapp.models import *
from article.models import *
from django_social_app import *
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event


class UserStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserStatus


class Event_CommentSerializer(serializers.ModelSerializer):
	commented_by = UserProfileSerializer()
	class Meta:
		model = Event_Comment


class CommentSerializer(serializers.ModelSerializer):
	commented_by = UserProfileSerializer()
	class Meta:
		model = Comment
