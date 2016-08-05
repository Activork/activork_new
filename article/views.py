from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import ArticleForm
from .models import Article,User_Stats,SimilarArticle
import ipgetter
import requests
from PIL import Image, ImageOps,ImageChops
from math import radians
from easy_thumbnails.files import get_thumbnailer
import urllib
from urlparse import urlparse
from django.core.files import File
import datetime
import pytz
from myapp.serializers import CommentSerializer
from django.contrib.auth.decorators import login_required

utc=pytz.UTC

def follow_user(request):
	if request.method == "POST" and request.is_ajax():
		user_id = request.POST["followed_by"]
		user_obj = UserProfile.objects.get(id=user_obj)
		obj = Follow_User(follow=request.user,followed_by=user_obj)
		obj.save()
		return HttpResponse("follow")


def unfollow_user(request):
	if request.method == "POST" and request.is_ajax():
                user_id = request.POST["unfollowed_by"]
                user_obj = UserProfile.objects.get(id=user_obj)
                obj = Follow_User.objects.get(follow=request.user,followed_by=user_obj)
                obj.delete()
		return HttpResponse("unfollow")
               


def rate_article(request):
	if request.method == "POST" and request.is_ajax():
		article_id = request.POST['article_id']
		rating = request.POST['rating']
		article_obj = Article.objects.get(id=article_id)
		userprofile_obj = UserProfile.objects.get(user=request.user)
		check = Like.objects.filter(article=article_obj,user=userprofile_obj).exists()

        	if check:
                	like_obj = Like.objects.get(article=article_obj,user=userprofile_obj)
			like_obj.rating = rating
                	like_obj.save()

		else:
			like_obj = Like(article=article_obj,user=userprofile_obj,rating=rating)
                	like_obj.save()

        return HttpResponse('success')


def comment_on_article(request):
		if request.is_ajax() and request.method == "POST":
                	article_id = request.POST['article_id']
                	article_obj = Article.objects.get(id=article_id)
                	comment = request.POST['comment']
                	userprofile_obj = UserProfile.objects.get(user=request.user)
                	comment_obj = Comment(article=article_obj,comment=comment,commented_by=userprofile_obj)
                	comment_obj.save()
                	article_comment_obj = Comment.objects.filter(article=article_obj)
                	serializer = CommentSerializer(article_comment_obj,many=True)
                	return HttpResponse(serializer.data)


@login_required
def like_article(request):
        article_id = request.POST['article_id']
        article_obj = Article.objects.get(id=article_id)
        userprofile_obj = UserProfile.objects.get(user=request.user)
        check = Like.objects.filter(article=article_obj,user=userprofile_obj).exists()

        if check:
                like_obj = Like.objects.get(article=article_obj,user=userprofile_obj)
		like_obj.like = True
                like_obj.save()
	else:
		like_obj = Like(article=article_obj,user=userprofile_obj,like=True)
		like_obj.save()
        return HttpResponseRedirect('/article_page/')


def save_similar_article(request):
	if request.method == "POST" and request.is_ajax():
		similar_id = int(request.POST['similar_id'])
		#return HttpResponse(similar_id)
		print similar_id
		if similar_id == 0:
			return HttpResponse("no saving")
		else:
			ids = request.POST.getlist('ids[]')

			print ids

			similar_obj = SimilarArticle.objects.get(id=similar_id)

			similar_obj.selected = ",".join(ids)

			similar_obj.save()
			
			return HttpResponse(similar_obj.selected)




def export_article(request):
	if request.method == "POST":
		similar_id = request.POST['similar_id']

		tag_list = request.POST.getlist('tags')

		search_tags = request.POST['search_tags']

		

		#search_tags += ","+",".join(tag_list)

		similar_obj = SimilarArticle.objects.get(id=similar_id)

		article_obj = Article.objects.get(id=similar_obj.article.id)

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

	else:
		article_id = request.GET.get('ids',None)
		if article_id != None:
			article_obj = Article.objects.get(id=article_id)
			similar_article_obj = SimilarArticle.objects.get_or_create(article=article_obj)
			similar_id = similar_article_obj[0].id
		else:
			similar_id = 0
		all_obj = Article.objects.all()

		

	return render(request,'article_query.html',{'article_objects':all_obj,'similar_id':similar_id,'article_obj':article_obj})




def home(request):
	if request.method=="POST":
		video_file = request.POST["video"]
		print "video_file",video_file
		print "share_with",request.POST['share_with']
		
		if video_file == "":	
			image = request.FILES['image']
			
		else:
			image = ""
			
			"""service = gdata.youtube.service.YouTubeService()
			feed_url = video_file
			feed = service.GetYouTubeVideoFeed(feed_url)
			print feed
			entry = feed.entry[0] # pick most viewed video as sample entry

			thumbnail = entry.media.thumbnail[0].url"""

			video_id = video_file.split("v=")[1]

			video_file = "https://www.youtube.com/embed/%s?rel=0&amp;controls=0"%video_id


			
			try:

				instance,created = Article.objects.get_or_create(video=video_file)

				if not created:
					return HttpResponseRedirect("/home")
			except:
				pass

			img_url = "http://img.youtube.com/vi/%s/0.jpg" % video_id
			file_name = urlparse(img_url).path.split('/')[-1]
			content = urllib.urlretrieve(img_url)
				
		myip = ipgetter.myip()
		url = 'http://freegeoip.net/json/'+myip
		r = requests.get(url)
		js = r.json()
		latitude = radians(js['latitude'])
		longitude = radians(js['longitude'])
		user = request.POST['posted_by']
		interest = request.POST['channels']
		name = request.POST['name']
		share_with = request.POST['share_with']

		name_tags = name.split(" ")

		exclude_tag_list = ['the','is','of','are','on','no','not']

		tags =[ i.lower() for i in name_tags if i not in exclude_tag_list and len(i) >= 4]

		tags = ",".join(tags)

		content_data = request.POST['content']
		obj = Article(content=content_data,video=video_file,image=image,latitude=latitude,longitude=longitude,tags=tags,posted_by=user,interest=interest,name=name,share_with=share_with)
		obj.save()
		if image == "":
			#file_name = str(file_name) + ".png"
			obj.image.save(file_name, File(open(content[0])), save=True)
			

		#image_file = Image.open(image)
		"""thumbnailer = get_thumbnailer(obj.image)
		thumbnail = thumbnailer.generate_thumbnail(thumbnail_options={
                                                'crop': True,
                                                'upscale': True,
                                                'size': (400,400)
                                                })
		image = thumbnail.image
		print obj.image.url"""


		"""image = Image.open(obj.image)
		width = image.size[0]
		height = image.size[1]

		aspect = width / float(height)

		ideal_width = 400
		ideal_height = 400"""
		"""
		ideal_aspect = ideal_width / float(ideal_height)

		if aspect > ideal_aspect:
    			# Then crop the left and right edges:
    			new_width = int(ideal_aspect * height)
    			offset = (width - new_width) / 2
    			resize = (offset, 0, width - offset, height)
		else:
    			# ... crop the top and bottom:
    			new_height = int(width / ideal_aspect)
    			offset = (height - new_height) / 2
    			resize = (0, offset, width, height - offset)

		thumb = image.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
		thumb.save(obj.image.url)"""

		"""image.thumbnail((400,400), Image.ANTIALIAS)


		image.save(obj.image.url)"""

		"""basewidth = 400
		img = Image.open(obj.image)
		wpercent = (basewidth/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((basewidth,hsize), Image.ANTIALIAS)
		img.save(obj.image.url)"""

		image = Image.open(obj.image)
		size = (400,400)
		image.thumbnail(size, Image.ANTIALIAS)
    		image_size = image.size

		pad = False

    		if pad:
        		thumb = image.crop( (0, 0, size[0], size[1]) )

        		offset_x = max( (size[0] - image_size[0]) / 2, 0 )
        		offset_y = max( (size[1] - image_size[1]) / 2, 0 )

        		thumb = ImageChops.offset(thumb, offset_x, offset_y)

    		else:
        		thumb = ImageOps.fit(image, size, Image.ANTIALIAS, (0.5, 0.5))

    		thumb.save(obj.image.url)


		#obj.save()

		return HttpResponseRedirect('/home')

	if request.method == "GET":
		form = ArticleForm()
		if len(Article.objects.all()) > 0:
			articles = Article.objects.all()
		else:
			articles = 0
		return render(request,'home.html',{'form':form,'articles':articles})



def article_page(request,article_id):
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


	return render(request,'article_page.html',{'all_comment':all_comment,'article_obj':obj,'like_count':like_count,'comment_count':comment_count,'rating':rating,'similar_article':similar_article})


def update_time(request):
	if request.is_ajax() and request.method == "POST":
		end_time = request.POST["end_time"]
		article_id = request.POST["article_id"]
		user_stat_obj = User_Stats.objects.get(article=article_id)
		
		earlier_duration = user_stat_obj.time_duration
		end_time = end_time.split(" ")
		end_time = datetime.datetime(int(end_time[0]), int(end_time[1]), int(end_time[2]), int(end_time[3]), int(end_time[4]), int(end_time[5])).replace(tzinfo=utc)

		user_stat_obj.end_time = end_time


		duration = end_time - user_stat_obj.start_time
		days, seconds = duration.days, duration.seconds
    		hours = days * 24 + seconds // 3600
    		minutes = (seconds % 3600) // 60
    		seconds = (seconds % 60)
		
		duration = str(hours) +" hours, "+str(minutes) +" minutes, " +str(seconds) +" seconds"
		

		print earlier_duration

		user_stat_obj.time_duration = duration
		
		user_stat_obj.save()		
		

		if earlier_duration > user_stat_obj.time_duration:
			user_stat_obj.time_duration = earlier_duration
			user_stat_obj.save()

		return HttpResponse(duration)
