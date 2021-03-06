from django.shortcuts import render,redirect,get_object_or_404
from .models import User_Details_Earlier,Event,SimilarEvent,User_Connection,Upload_Image,UserProfile,UserStatus, Event_Liked
from notifications.signals import notify
from django.http import HttpResponseRedirect, HttpResponse
from social.apps.django_app.default.models import UserSocialAuth
import requests
from .forms import Upload_ImageForm
import os
from PIL import Image
import shutil
import ipgetter
import requests
from rest_framework.decorators import api_view
from django_social_app.views import get_user_object 
from django.contrib.auth.decorators import login_required
from article.models import *
from .serializers import *
from rest_framework.response import Response
import math
import re




@api_view(['GET'])
def mobile_earlier_home_page(request):
	device_id = request.GET.get('device_id','1')
	user_detail_obj = User_Details_Earlier.objects.get(info=device_id)
	articles = []
	for i in user_detail_obj.interest:
		 articles += Article.objects.filter(interest__contains=i)

	article = set(articles)
	
	event = []
	for i in user_detail_obj.interest:
		event += Event.objects.filter(interest__contains=i)


	event  = set(event)

	#user_friend = User_Connection.objects.filter(sender__user=user,receiver__user=user)

	"""all_event = {}
	for j in event:
		all_event[j] = []
		interested_events = Event_Liked.objects.filter(event=i).filter(user__user__in=user_friend,going=True).values_list('user',flat=True)[:5]

	for i,j in all_event.iteritems():
		if len(j) == 0:
			j = Event_Liked.objects.filter(event=j).order_by('-id').values_list('user',flat=True)[:5] 
		else:
			j += Event_Liked.objects.filter(event=j).order_by('-id').values_list('user',flat=True)[len(j):5]"""
	
	all_article_data = []
	
	for i in article:
		print i
		all_article = {}
		all_article['article'] = {}
		serializer_article = ArticleSerializer(i)
		all_article['article']['article_details'] = serializer_article.data
		all_article['article']['like'] =  Like.objects.filter(article=i).count()
		all_article['article']['comment'] = Comment.objects.filter(article=i).count()		
		all_article_data.append(all_article['article'])

	event_dict = {}

	event_data = []	
	for i in event:
		event_dict['event'] = {}
		serializer_event=EventSerializer(i)
		event_dict['event']['event_details'] = serializer_event.data
		event_data.append(event_dict['event'])

	return Response({'all_article':all_article_data,'all_event':event_data})

@api_view(['POST'])
@get_user_object
def mobile_fill_userprofile(request):
	if request.method == "POST":
		user = request.user
		keys = request.data.keys()
		check = UserProfile.objects.filter(user=request.user).exists()


		if check:
			userprofile_obj = UserProfile.objects.get(user=request.user)
			for j in keys:
				#print "key",j
				if j == "age":
					print "age",request.data['age']
					userprofile_obj.age = request.data['age']
					continue
				if j == "designation":
					userprofile_obj.designation = request.data[j] 	
					continue
				if j == "working_at":
					userprofile_obj.working_at = request.data[j]
					continue

				if j == "profile_image":	
					userprofile_obj.profile_image = request.data[j]
					continue

				if j == "college":
					userprofile_obj.college = request.data[j]
					continue

				if j == "channels":
					ch = request.data.getlist('channels')
					if len(ch) >= 1:
						channels = []
						for i in ch[0].split(","):
                                        		if i == "Travel":
                                                		channels.append("item_key1")
                                        		elif i == "Fitness":
                                                		channels.append("item_key2")
                                        		elif i == "Music":
                                                		channels.append("item_key3")
                                        		elif i == "Hobbies":
                                                		channels.append("item_key4")
                                        		else:
                                                		channels.append("item_key5")
                                		channels = ",".join(channels)
						userprofile_obj.channels =channels
		


			userprofile_obj.save()
			#print userprofile_obj.age
			return Response("updated profile")

		else:
			profile_image = request.data['profile_image']
			age = request.data['age']
			designation = request.data['designation']
			try:
				ch = request.data.getlist('channels')
			except:
				ch = []
	
			if len(ch) >= 1:
				print "in"
				channels = []
				for i in ch[0].split(","):
					if i == "Travel":
                                        	channels.append("item_key1")
                                	elif i == "Fitness":
                                        	channels.append("item_key2")
                                	elif i == "Music":
                                        	channels.append("item_key3")
                                	elif i == "Hobbies":
                                        	channels.append("item_key4")
                                	else:
                                        	channels.append("item_key5")
				channels = ",".join(channels)
			else:
				return Response("Please select interests")
		
			print channels

			working_at = request.data['working_at']
			college = request.data['college']
			about = request.data['about']

			if len(ch) >= 1:
				userprofile_obj = UserProfile(user=user,profile_image=profile_image,age=age,designation=designation,channels=channels,working_at=working_at,college=college,about=about)
			userprofile_obj.save()

		return Response("success")


@api_view(['POST'])
@get_user_object
def mobile_follow_user(request):
        if request.method == "POST":
                user_id = request.data["followed_by"]
		user_id = MyUser.objects.get(id=user_id)
                user_obj = UserProfile.objects.get(user=user_id)
		follow = UserProfile.objects.get(user=request.user)
                obj = Follow_User(follow=follow,followed_by=user_obj)
                obj.save()
                return Response("follow")


@api_view(['POST'])
@get_user_object
def mobile_unfollow_user(request):
        if request.method == "POST":
                user_id = request.data["unfollowed_by"]
		user_id = MyUser.objects.get(id=user_id)
                user_obj = UserProfile.objects.get(user=user_id)
		follow = UserProfile.objects.get(user=request.user)
                obj = Follow_User.objects.get(follow=follow,followed_by=user_obj)
                obj.delete()
                return Response("unfollow")



@api_view(['POST'])
@get_user_object
def mobile_rate_article(request):
	article_id = request.data['article_id']
	rating = float(request.data['rating'])
	#print "rating",rating,round(rating)
	rating = round(rating)
	article_obj = Article.objects.get(id=article_id)

	check = UserProfile.objects.filter(user=request.user).exists()

	if not check:
		return Response("Plase fill your profile first")


	userprofile_obj = UserProfile.objects.get(user=request.user)
	check = Like.objects.filter(article=article_obj,user=userprofile_obj).exists()

        if check:
                like_obj = Like.objects.get(article=article_obj,user=userprofile_obj)
		like_obj.rating = rating
                like_obj.save()

	else:
		like_obj = Like(article=article_obj,user=userprofile_obj,rating=rating)
                like_obj.save()

        return Response('success')




@api_view(['GET'])
@get_user_object
def mobile_article_page(request,article_id):
	obj = Article.objects.get(id=article_id)
	check = User_Stats.objects.filter(article=article_id).exists()

	if not check:
		user_stat_obj = User_Stats(article=obj,time_duration=datetime.timedelta(minutes=1))
		user_stat_obj.save()

	else:
		user_stat_obj = User_Stats.objects.get(article=article_id)
		user_stat_obj.start_time = datetime.datetime.now().replace(tzinfo=utc)
		user_stat_obj.save()

	like_check = Like.objects.filter(article=obj).exists()
	comment_check = Comment.objects.filter(article=obj).exists()

	if like_check:
		like_count = len(Like.objects.filter(article=obj,like=True))
		all_rating = Like.objects.filter(article=obj).values_list('rating',flat=True)
		rating = sum(all_rating)/len(all_rating)
	else:
		like_count = 0
		rating = 1


	if comment_check:
		all_comment = Comment.objects.filter(article=obj)
		comment_count = len(all_comment)
	else:
		comment_count = 0
		all_comment = 0

	
	similar_obj = SimilarArticle.objects.get(article=obj)
	similar_article = []

	for i in similar_obj.selected.split(","):
		similar_article +=  Article.objects.filter(id=i)

	similar_serializer = ArticleSerializer(similar_article,many=True)
	obj_serializer = ArticleSerializer(obj)

	comment_serializer = CommentSerializer(all_comment,many=True)

	return Response({'all_comment':comment_serializer.data,'article_obj':obj_serializer.data,'like_count':like_count,'comment_count':comment_count,'rating':rating,'similar_article':similar_serializer.data})



@api_view(['GET'])
@get_user_object
def mobile_event_page(request,event_id):
	event_obj = Event.objects.get(id=event_id)
	going_check = Event_Liked.objects.filter(event=event_obj).exists()
	comment_check = Event_Comment.objects.filter(event=event_obj).exists()

	if going_check:
		going_count = len(Event_Liked.objects.filter(event=event_obj,going=True))
		maybe_count = len(Event_Liked.objects.filter(event=event_obj,like=True))
	else:
		going_count = 0
		maybe_count = 0


	if comment_check:
		all_comment = Event_Comment.objects.filter(event=event_obj)
		comment_count = len(all_comment)
	else:
		comment_count = 0
		all_comment = 0

	similar_obj = SimilarEvent.objects.get(event=event_obj)
	similar_event = []

	for i in similar_obj.selected.split(","):
		similar_event += Event.objects.filter(id=i)


	user_friend = User_Connection.objects.filter(sender__user=user,receiver__user=user)

	
	friends_going = Event_Liked.objects.filter(event=event_obj).filter(user__user__in=user_friend,going=True).values_list('user',flat=True)[:5]


	if len(friends_going) == 0:
		friends_going = Event_Liked.objects.filter(event=event_obj).order_by('-id').values_list('user',flat=True)[:5]


	similar_serializer = EventSerializer(similar_event,many=True)
	obj_serializer = EventSerializer(obj)

	comment_serializer = Event_CommentSerializer(all_comment,many=True)

	friends_going = UserProfileSerialzer(friends_going,many=True)

	return Response({'all_comment':comment_serializer.data,'event_obj':event_obj.serializer,'going_count':going_count,'maybe_count':maybe_count,'comment_count':comment_count,'similar_event':similar_event,'friends_going':friends_going.data})


@login_required
def like_event(request):
	event_id = request.POST['event_id']
	event_obj = Event.objects.get(id=event_id)
	userprofile_obj = Userprofile.objects.get(user=request.user)
	check = Event_Liked.objects.filter(event=event_obj,user=userprofile_obj).exists()

	if check:
		event_liked_obj = Event_Liked.objects.get(event=event_obj,user=userprofile_obj)
		event_liked_obj.like = True
		event_liked_obj.save()

	else:
		event_liked_obj = Event_Liked(user=userprofile_obj,event=event_obj,like=True)
		event_liked_obj.save()
	return HttpResponseRedirect('/event_page/')


@api_view(['POST'])
@get_user_object
def mobile_like_event(request):
        event_id = request.data['event_id']
        event_obj = Event.objects.get(id=event_id)

	check = UserProfile.objects.filter(user=request.user).exists()

        if not check:
                return Response("Please fill your profile first")



        userprofile_obj = UserProfile.objects.get(user=request.user)
        check = Event_Liked.objects.filter(event=event_obj,user=userprofile_obj).exists()

        if check:
                event_liked_obj = Event_Liked.objects.get(event=event_obj,user=userprofile_obj)
                event_liked_obj.like = True
                event_liked_obj.save()

        else:
                event_liked_obj = Event_Liked(user=userprofile_obj,event=event_obj,like=True)
                event_liked_obj.save()
        return Response("success")



def comment_on_event(request):
	if request.is_ajax() and request.method == "POST":
		event_id = request.POST['event_id']
		event_obj = Event.objects.get(id=event_id)
		comment = request.POST['comment']
		userprofile_obj = UserProfile.objects.get(user=request.user)
		comment_obj = Event_Comment(event=event_obj,comment=comment,commented_by=userprofile_obj)
		comment_obj.save()
		event_comment_obj = Event_Comment.objects.filter(event=event_obj)
		serializer = Event_CommentSerializer(event_comment_obj,many=True)
		return HttpResponse(serializer.data)


@api_view(['POST','GET'])
@get_user_object
def mobile_comment_on_event(request):
		if request.method == "POST":
                	event_id = request.data['event_id']
                	event_obj = Event.objects.get(id=event_id)
                	comment = request.data['comment']

			check = UserProfile.objects.filter(user=request.user).exists()
			if not check:
				return Response("Please fill your profile first")
			if not re.search(r'^[a-zA-Z]+',comment,re.I):
				return Response("Please enter a comment")



                	userprofile_obj = UserProfile.objects.get(user=request.user)
                	comment_obj = Event_Comment(event=event_obj,comment=comment,commented_by=userprofile_obj)
                	comment_obj.save()
                	event_comment_obj = Event_Comment.objects.filter(event=event_obj)
                	serializer = Event_CommentSerializer(event_comment_obj,many=True)
                	return Response({'comments':serializer.data})


		if request.method == "GET":

			event_id = request.GET['event_id']
                        event_obj = Event.objects.get(id=event_id)

			event_comment_obj = Event_Comment.objects.filter(event=event_obj)

			if len(event_comment_obj) == 0:
                                return Response("No comments yet")


			if len(event_comment_obj) > 1:
                        	serializer = Event_CommentSerializer(event_comment_obj,many=True)
			else:
				serializer = Event_CommentSerializer(event_comment_obj)
                        return Response({'comments':serializer.data})




@api_view(['POST','GET'])
@get_user_object
def mobile_comment_on_article(request):
		if request.method == "POST":
                	article_id = request.data['article_id']
                	article_obj = Article.objects.get(id=article_id)
                	comment = request.data['comment']

			check = UserProfile.objects.filter(user=request.user).exists()

			if not check:
				return Response("Please fill your profile first")
	
			if not re.search(r'^[a-zA-Z]+',comment,re.I):
				return Response("Please enter a comment")

                	userprofile_obj = UserProfile.objects.get(user=request.user)
                	comment_obj = Comment(article=article_obj,comment=comment,commented_by=userprofile_obj)
                	comment_obj.save()
                	article_comment_obj = Comment.objects.filter(article=article_obj)
                	serializer = CommentSerializer(article_comment_obj,many=True)
                	return Response({'comments':serializer.data})

		if request.method == "GET":
			article_id = request.GET['article_id']
                        article_obj = Article.objects.get(id=article_id)
			article_comment_obj = Comment.objects.filter(article=article_obj)

			if len(article_comment_obj) == 0:
				return Response("No comments yet")


			if len(article_comment_obj) > 1:
                        	serializer = CommentSerializer(article_comment_obj,many=True)
			else:
				serializer = CommentSerializer(article_comment_obj)           
                        return Response({'comments':serializer.data})



@api_view(['POST'])
@get_user_object
def mobile_like_article(request):
	article_id = request.data['article_id']
	article_obj = Article.objects.get(id=article_id)
	check = UserProfile.objects.filter(user=request.user).exists()

	if not check:
		return Response("Please fill your profile first")

	userprofile_obj = UserProfile.objects.get(user=request.user)
	check = Like.objects.filter(article=article_obj,user=userprofile_obj).exists()

        if check:
                like_obj = Like.objects.get(article=article_obj,user=userprofile_obj)
		like_obj.like = True
                like_obj.save()
	else:
		like_obj = Like(article=article_obj,user=userprofile_obj,like=True)
		like_obj.save()

        return Response('success')





@api_view(['POST'])
@get_user_object
def mobile_going_event(request):
        event_id = request.data['event_id']
        event_obj = Event.objects.get(id=event_id)

	check = UserProfile.objects.filter(user=request.user).exists()

	if not check:
		return Response("Please fill your profile first")


        userprofile_obj = UserProfile.objects.get(user=request.user)
        check = Event_Liked.objects.filter(event=event_obj,user=userprofile_obj).exists()

        if check:
                event_liked_obj = Event_Liked.objects.get(event=event_obj,user=userprofile_obj)
                event_liked_obj.going = True
                event_liked_obj.save()

        else:
                event_liked_obj = Event_Liked(user=userprofile_obj,event=event_obj,going=True)
                event_liked_obj.save()
        return Response("success")




@login_required
def going_event(request):
        event_id = request.POST['event_id']
        event_obj = Event.objects.get(id=event_id)
        userprofile_obj = Userprofile.objects.get(user=request.user)
        check = Event_Liked.objects.filter(event=event_obj,user=userprofile_obj).exists()

        if check:
                event_liked_obj = Event_Liked.objects.get(event=event_obj,user=userprofile_obj)
                event_liked_obj.going = True
                event_liked_obj.save()

        else:
                event_liked_obj = Event_Liked(user=userprofile_obj,event=event_obj,going=True)
                event_liked_obj.save()
        return HttpResponseRedirect("/event_page/")




@login_required
def update_status(request):
	user=request.user
	userprofile = UserProfile.objects.get(user=user)
	check = UserStatus.objects.filter(user=userprofile).exists()
	status = request.POST['status']
	public = request.POST['public']
	
	if check:
		status_obj = UserStatus.objects.filter(user=userprofile)
		status_obj.status = status
		status_obj.public = public
		status_obj.save()

	else:
		status_obj = UserStatus(user=userprofile,status=status,public=public)
		status_obj.save()

	return HttpResponse(status_obj.status)


@api_view(['POST'])
@get_user_object
def mobile_update_status(request):
	user=request.user
	#return Response({"name":user.username})
	check = UserProfile.objects.filter(user=user).exists()
	if not check:
		return Response("complete your profile first")
	userprofile = UserProfile.objects.get(user=user)
	check = UserStatus.objects.filter(user=userprofile).exists()
	status = request.data['status']
	try:
		public = request.data['public']
	except:
		public = ""
	
	
	if check:
		status_obj = UserStatus.objects.get(user=userprofile)
		status_obj.status = status
		if public != "":
			status_obj.public = public
		status_obj.save()

	else:
		if public != "":
			status_obj = UserStatus(user=userprofile,status=status,public=public)
		else:
			status_obj = UserStatus(user=userprofile,status=status)
		status_obj.save()

	serializer_userstatus = UserStatusSerializer(status_obj)

	return Response({'status_obj':serializer_userstatus.data})



@login_required
def home_page(request):
	user =request.user
	user_detail_obj = User_Details.objects.get(user=user)
	all_article = []
	for i in user_detail_obj.interest:
		 article += Article.objects.filter(interest__contains=i)

	article = [set(all_article)]
	
	all_article = []

	for i in article:
		all_article[i] = []
		like = Like.objects.filter(article=i).count()
		comment = Comment.objects.filter(article=i).count()
		all_article[i] = [like,comment]

	all_event = []
	for i in user_detail_obj.interest:
		event += Event.objects.filter(interest__contains=i)

	event  = [set(event)]

	user_friend = User_Connection.objects.filter(sender__user=user,receiver__user=user)

	all_event = {}
	for j in event:
		all_event[j] = []
		interested_events = Event_Liked.objects.filter(event=i).filter(user__user__in=user_friend,going=True).values_list('user',flat=True)[:5]

	for i,j in all_event.iteritems():
		if len(j) == 0:
			j = Event_Liked.objects.filter(event=j).order_by('-id').values_list('user',flat=True)[:5] 
		else:
			j += Event_Liked.objects.filter(event=j).order_by('-id').values_list('user',flat=True)[len(j):5]

	return render(request,'home_page.html',{'all_article':article,'all_event':all_event})




@api_view(['GET'])
@get_user_object
def mobile_home_page(request):
	user =request.user
	user_detail_obj = User_Details.objects.get(user=user)
	all_article = []
	for i in user_detail_obj.interest:
		 all_article += Article.objects.filter(interest__contains=i)

	article = [set(all_article)]
	
	all_event = []
	for i in user_detail_obj.interest:
		event += Event.objects.filter(interest__contains=i)

	event  = [set(event)]

	user_friend = User_Connection.objects.filter(sender__user=user,receiver__user=user)

	all_event = {}
	for j in event:
		all_event[j] = []
		interested_events = Event_Liked.objects.filter(event=i).filter(user__user__in=user_friend,going=True).values_list('user',flat=True)[:5]

	for i,j in all_event.iteritems():
		if len(j) == 0:
			j = Event_Liked.objects.filter(event=j).order_by('-id').values_list('user',flat=True)[:5] 
		else:
			j += Event_Liked.objects.filter(event=j).order_by('-id').values_list('user',flat=True)[len(j):5]
	
	all_article = {}
	for i in article:
		serializer_article = ArticleSerializer(i,many=True)
		all_article['article']['article_details'] = serializer_article.data
		all_article['article']['like'] =  Like.objects.filter(article=i).count()
		all_article['article']['comment'] = Comment.objects.filter(article=i).count()		


	event_dict = {}
	
	for i,j in all_event.iteritems():
		serializer_event=EventSerializer(i)
		serializer_userprofile = UserProfileSerializer(j,many=True)
		event_dict['event']['event_details'] = serializer_event.data
		event_dict['event']['event_users'] = serializer_userprofile.data

	return Response({'all_article':all_article,'all_event':event_data})


def get_details(request):
	if request.method == "POST":
		#interests = request.POST.getlist('interests')
		myip = ipgetter.myip()
                url = 'http://freegeoip.net/json/'+myip
                r = requests.get(url)
                js = r.json()
                latitude = radians(js['latitude'])
                longitude = radians(js['longitude'])
		check = User_Details_Earlier.objects.filter(info=myip).exists()

		if not check:
			obj = User_Details_Earlier(info=myip,latitude=latitude,longitude=longitude)
			obj.save()
		else:
			obj = User_Details_Earlier.objects.get(info=myip)
			interests = request.POST.getlist('interests')
                        interests_key = []
                        for i in interests[0].split(","):
				interests_key.append(i)
                        interests_key = ",".join(interests_key)

                        print interests_key

                        obj.interest = interests_key
			obj.save()

		return HttpResponseRedirect('/get_details')

@api_view(['POST'])
def mobile_get_details(request):
        if request.method == "POST":

		device_id = request.data['device_id']
                check = User_Details_Earlier.objects.filter(info=device_id).exists()

                if not check:
			latitude = request.data['latitude']
			longitude = request.data['longitude']
                        obj = User_Details_Earlier(info=device_id,latitude=latitude,longitude=longitude)
                        obj.save()
                else:
                        obj = User_Details_Earlier.objects.get(info=device_id)
			latitude = request.data['latitude']
			longitude = request.data['longitude']

			try:
				print "in",request.data['interests']
				interests = request.data.getlist('interests')

			except:
				interests = []


			interests_key = []
			print "list",interests
			
			if len(interests) >=1:
			   for i in interests[0].split(","):
				if i == "Travel":
					interests_key.append("item_key1")
				elif i == "Fitness":
					interests_key.append("item_key2")
				elif i == "Music":
					interests_key.append("item_key3")
				elif i == "Hobbies":
					interests_key.append("item_key4")
				elif i == "Momentum":
					interests_key.append("item_key5")
				else:
					return Response({"error":"Please select a valid channel"})

			interests_key = ",".join(interests_key)

			print interests_key

			if len(interests_key) >= 1:								obj.interest = interests_key
			obj.latitude = latitude
			obj.longitude = longitude

                        obj.save()
			print obj.interest
			return Response("interests updated")
		
                return Response("success")
		


@api_view(['POST'])
@get_user_object
def mobile_get_info(request):
        if request.method == "POST":
		
		user = request.user
		print "user",user

                check = User_Details.objects.filter(user=user.id).exists()

                if not check:
			latitude = request.data['latitude']
			longitude = request.data['longitude']
                        obj = User_Details(user=user,latitude=latitude,longitude=longitude)
                        obj.save()
                else:
                        obj = User_Details.objects.get(user=user)
			latitude = request.data['latitude']
			longitude = request.data['longitude']

			try:
				print "in",request.data['interests']
				interests = request.data.getlist('interests')
			except:
				interests = []
			interests_key = []
			print "list",interests

			if len(interests) >=1:
			  for i in interests[0].split(","):
				if i == "Travel":
					interests_key.append("item_key1")
				elif i == "Fitness":
					interests_key.append("item_key2")
				elif i == "Music":
					interests_key.append("item_key3")
				elif i == "Hobbies":
					interests_key.append("item_key4")
				else:
					interests_key.append("item_key5")

			interests_key = ",".join(interests_key)

			print interests_key

			if len(interests_key) >=1:
                        	obj.interest = interests_key
			obj.latitude = latitude
			obj.longitude = longitude
                        obj.save()
			print obj.interest
			return HttpResponse("interests updated")
		
                return HttpResponse("success")




def save_similar_event(request):
        if request.method == "POST" and request.is_ajax():
                similar_id = int(request.POST['similar_id'])
                print similar_id
                if similar_id == 0:
                        return HttpResponse("no saving")
                else:
                        ids = request.POST.getlist('ids[]')

                        print ids

			#NOt implemented depending upon distance


			check =  SimilarEvent.objects.filter(event=similar_id).exists()
                        if check:

                                similar_obj = SimilarEvent.objects.get(event=similar_id)
                        else:
                                event = Event.objects.get(id=similar_id)
                                similar_obj = SimilarEvent(event=event)


                       # similar_obj = SimilarEvent.objects.get(id=similar_id)

                        similar_obj.selected = ",".join(ids)

                        similar_obj.save()

                        return HttpResponse(similar_obj.selected)




def export_event(request):
        if request.method == "POST":
                similar_id = request.POST['similar_id']
                search_tags = request.POST['search_tags']

                print search_tags

		tag_list = request.POST.getlist('tags')


		similar_obj = SimilarEvent.objects.get(id=similar_id)

                event_obj = Event.objects.get(id=similar_obj.event.id)

                print search_tags

                if search_tags != "":
                        tags= [i for i in search_tags.split(",")]
                else:
                        tags = []

                tags.extend(tag_list)

                print tags
                all_obj = []

                for i in tags:
                        all_values = Article.objects.all()
                        for j in all_values:
                                if i in j.tags:
                                        if j not in all_obj:
                                                all_obj += [j]


                """tags= [i for i in search_tags.split(",")]

                print tags
                all_obj = []

                for i in tags:
                        all_values = Event.objects.all()
                        for j in all_values:
                                if i in j.tags:
                                        all_obj += [j]"""

        else:
                event_id = request.GET.get('ids',None)

		print "event_id",event_id
                if event_id != None:
                        event_obj = Event.objects.get(id=event_id)

			similar_event_obj = SimilarEvent.objects.get_or_create(event=event_obj)
                        similar_id = similar_event_obj[0].id
                else:
                        similar_id = 0
                all_obj = Event.objects.all()
        return render(request,'event_query.html',{'event_obj':event_obj,'event_objects':all_obj,'similar_id':similar_id})



def notifications(request):
	user_info = UserProfile.objects.get(user=request.user)
	get_receiver_ids = list(User_Connection.objects.filter(sender=user_info).values_list("receiver",flat=True))		
	get_sender_ids = list(User_Connection.objects.filter(receiver=user_info).values_list("sender",flat=True))

	
	get_sender_ids.extend(get_receiver_ids)

	total_ids = [i for i in get_sender_ids]
	if len(total_ids) != 0:
		last_regular_suugested_id = max(total_ids)
		get_next_id = last_regular_suggested_id +1 
	else:
		get_next_id = 1
	return render(request,'notification.html',{'user_info':user_info,'get_next_id':get_next_id})



def messages(request):
        user_info = UserProfile.objects.get(user=request.user)
	get_receiver_ids = list(User_Connection.objects.filter(sender=user_info).values_list("receiver",flat=True))		
	get_sender_ids = list(User_Connection.objects.filter(receiver=user_info).values_list("sender",flat=True))

	
	get_sender_ids.extend(get_receiver_ids)

	total_ids = [i for i in get_sender_ids]
	if len(total_ids) != 0:
		
		get_next_id = max(total_ids) +1 
	else:
		get_next_id = 1
        return render(request,'messages.html',{'user_info':user_info,'get_next_id':get_next_id})



def settings(request):
	user_info = UserProfile.objects.get(user=request.user)
	get_receiver_ids = list(User_Connection.objects.filter(sender=user_info).values_list("receiver",flat=True))		
	get_sender_ids = list(User_Connection.objects.filter(receiver=user_info).values_list("sender",flat=True))

	
	get_sender_ids.extend(get_receiver_ids)

	total_ids = [i for i in get_sender_ids]
	if len(total_ids) != 0:
		
		get_next_id = max(total_ids) +1 
	else:
		get_next_id = 1
	return render(request,'settings.html',{'user_info':user_info,'get_next_id':get_next_id})


def self_profile(request):
	check = UserProfile.objects.filter(user=request.user).exists()
	if check:
		current_user = UserProfile.objects.get(user=request.user)
		crop_obj = Upload_Image.objects.get(user=request.user)
	else:
		check_social_acc = UserSocialAuth.objects.filter(user=request.user).exists()
		if not check_social_acc:
			current_user = UserProfile(user=request.user,profile_image="profile_photos/defaultuser.png",designation="")
			current_user.save()
			crop_obj = Upload_Image(user=request.user,image="profile_photos/defaultuser.png")
			crop_obj.save()
		else:
			social_obj = UserSocialAuth.objects.get(user=request.user)
			if social_obj.provider == "facebook":
				
				email = social_obj.extra_data["email"]
				first_name = social_obj.extra_data["first_name"]
				last_name = social_obj.extra_data["last_name"]
				
				uid = social_obj.uid
				url = "http://graph.facebook.com/{0}/picture?type=large".format(uid)

				response = requests.get(url, stream=True,verify=False)
				with open("profile_photos/img"+str(request.user.id)+".png", 'wb') as out_file:
    					shutil.copyfileobj(response.raw, out_file)
				del response

			social_obj.user.email = email
			social_obj.user.first_name = first_name
			social_obj.user.last_name = last_name
			social_obj.user.save()	

			current_user = UserProfile(user=request.user,profile_image="profile_photos/img"+str(request.user.id)+".png",designation="")
			current_user.save()
			crop_obj = Upload_Image(user=request.user,image="profile_photos/img"+str(request.user.id)+".png")
			crop_obj.save()


	if request.method == 'POST':
            
            print request.FILES
	    request.POST['user'] = request.user.id
	    print request.POST
            form = Upload_ImageForm(request.POST, request.FILES, instance=crop_obj)
            if form.is_valid():
                form.save()		
		current_user.profile_image = crop_obj.image
		print current_user.profile_image
		current_user.save()
		path = current_user.profile_image.url
		location = path.split("/")
		new_path = os.path.realpath("profile_photos")
		actual_path = new_path + "/" + location[-1]
		size = os.path.getsize(actual_path)
	
		if size > 100000:
			basewidth=300
			image = Image.open(path)
		
			if image.size[1]>300:
				wpercent = (basewidth/float(image.size[0]))
				hsize = int((float(image.size[1])*float(wpercent)))
				image.thumbnail((basewidth,hsize),Image.ANTIALIAS)
		
			
			if image.mode != 'RGB':
				image.convert('RGB')
			image.save(path,optimized=True,quality=75)

		if size < 10000:

			
			print path
			
			print "location",location
			
			print actual_path
			cmd = "convert -contrast -enhance -density 500 -normalize -quality 100 "+actual_path+" "+actual_path+""
			os.system(cmd)


	    else:
		print form.errors


	friends = []
	friends += User_Connection.objects.filter(sender__user=request.user,interest_status=1).values_list('receiver',flat=True)
	friends += User_Connection.objects.filter(receiver__user=request.user,interest_status=1).values_list('sender',flat=True)

	my_friends = UserProfile.objects.filter(user__in=friends)
	
	#print my_friends	

	current_user_hangouts = Hangout_Liked.objects.filter(user__in=friends)
	current_user_events = Event_Liked.objects.filter(user__in=friends)

	certified_hangouts = Hangout_Liked.objects.filter(user=request.user,regular=True)

	certified_events = Event_Liked.objects.filter(user=request.user,regular=True)

	#print current_user_events


	certified_event = {}
	certified_hangout = {}
	
	event_dict = {}
	hangout_dict = {}
	for i in current_user_hangouts:
		hangout_dict[i] = []
		regular_hangout = Hangout_Liked.objects.filter(hangout=i.hangout,regular=True).order_by('-id')[:7]
		hangout_dict[i] = regular_hangout

	event_dict = {}
	for i in current_user_events:
		event_dict[i] = []
        	regular_event = Event_Liked.objects.filter(event=i.event,regular=True).order_by('-id')[:7]
		print regular_event
		event_dict[i] = regular_event
	
	print event_dict

	
	for i in certified_hangouts:
                certified_hangout[i] = []
                regular_hangout = Hangout_Liked.objects.filter(hangout=i.hangout,regular=True).order_by('-id')[:7]
                certified_hangout[i] = regular_hangout

        for i in certified_events:
                certified_event[i] = []
                regular_event = Event_Liked.objects.filter(event=i.event,regular=True).order_by('-id')[:7]
                print regular_event
                certified_event[i] = regular_event

	get_receiver_ids = list(User_Connection.objects.filter(sender=current_user).values_list("receiver",flat=True))		
	get_sender_ids = list(User_Connection.objects.filter(receiver=current_user).values_list("sender",flat=True))

	
	get_sender_ids.extend(get_receiver_ids)

	total_ids = [i for i in get_sender_ids]
	print total_ids
	if len(total_ids) != 0:
		
		get_next_id = max(total_ids) +1 
	else:
		get_next_id = 1

	image = get_object_or_404(Upload_Image, id=crop_obj.id) if crop_obj.id else None
	form = Upload_ImageForm(instance=crop_obj)
	print crop_obj.image

	return render(request,'self_profile.html',{'get_next_id':get_next_id,'image':crop_obj,'my_friends':my_friends,'form':form,'certified_hangout':certified_hangout,'certified_event':certified_event,'hangout_dict':hangout_dict,'event_dict':event_dict,'user_info':current_user})

