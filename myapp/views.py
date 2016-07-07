from django.shortcuts import render,redirect,get_object_or_404
from .models import User_Connection,Upload_Image,UserProfile,UserStatus,Hangout_Liked, Event_Liked
from notifications.signals import notify
from django.http import HttpResponseRedirect, HttpResponse
from social.apps.django_app.default.models import UserSocialAuth
import requests
from .forms import Upload_ImageForm
import os
from PIL import Image
import shutil

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

