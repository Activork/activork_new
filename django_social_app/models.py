from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from django import forms


class MyUser(AbstractUser):
    phone_no = models.CharField(max_length=10)
    


class MyUserSerializer(serializers.ModelSerializer):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = MyUser

