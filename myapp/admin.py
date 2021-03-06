from django.contrib import admin
from django.contrib.auth.models import Permission
#from .models import Upload_Image,User_Connection,UserStatus,UserProfile,ProfileLimitation,Hangout,Event,Event_ImageGallery,SimilarEvent,Event_Staff,EventPermission, Event_Liked
from django.db.models import Q
from .forms import Event_StaffForm
from django_social_app.models import MyUser
from image_cropping.admin import ImageCroppingMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import *




class HangoutAdmin(admin.ModelAdmin):

	pass

	"""def formfield_for_foreignkey(self, db_field, request, **kwargs):
                #Limit choices for 'hangout' field to only your places.
                if db_field.name == 'owner':
                        if not request.user.is_superuser:
                                kwargs["queryset"] = MyUser.objects.filter(is_staff=True)
                return super(HangoutAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)"""


	"""def save_model(self, request, obj, form, change):
                if request.user.is_superuser:
			pl = Permission.objects.filter(codename__in=["add_hangoutpermission","change_hangoutpermission","delete_hangoutpermission","add_hangout_imagegallery", "change_hangout_imagegallery", "delete_hangout_imagegallery","change_hangout","change_hangout_staff","add_hangout_staff","add_hangout_promotion","change_hangout_promotion"])
                        obj.owner.user_permissions.add(*pl)
                        obj.owner.is_staff = True
                        obj.owner.save()
                        obj.save()"""


	"""def queryset(self, request):
        	qs = super(HangoutAdmin, self).queryset(request)
        	if request.user.is_superuser:
            		return qs

		get_user = HangoutPermission.objects.filter(access=request.user).values_list('hangout__owner',flat=True)
        	return qs.filter(Q(owner=request.user)|Q(owner=get_user))"""



class EventAdmin(admin.ModelAdmin):

	search_fields = ['name']
	actions = ['export_selected_objects']


	def export_selected_objects(self, request, queryset):
		selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		ct = ContentType.objects.get_for_model(queryset.model)
		print admin.ACTION_CHECKBOX_NAME
		print selected
		print queryset.model
		#return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
		return HttpResponseRedirect("/export/event/?ct=%s&ids=%s"%(ct.pk,",".join(selected)))


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                """Limit choices for 'place' field to only your places."""
                if db_field.name == 'organizer':
                        if not request.user.is_superuser:
                                kwargs["queryset"] = MyUser.objects.filter(is_staff=True)
                return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	def save_model(self, request, obj, form, change):
                if request.user.is_superuser:
                        pl = Permission.objects.filter(codename__in=["add_eventpermission","change_eventpermission","delete_eventpermission","add_event_imagegallery", "change_event_imagegallery", "delete_event_imagegallery","change_event","change_event_staff","add_event_staff","add_event_promotion","change_event_promotion"])
                        obj.organizer.user_permissions.add(*pl)
                        obj.organizer.is_staff = True
                        obj.organizer.save()
                        obj.save()



	def queryset(self,request):
		qs = super(EventAdmin,self).queryset(request)
		if request.user.is_superuser:
			return qs

		get_user = EventPermission.objects.filter(access=request.user).values_list('event__organizer',flat=True)
		return qs.filter(Q(organizer=request.user)|Q(organizer=get_user))
	

"""class Hangout_ImageGalleryAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
        	#Limit choices for 'place' field to only your places.
        	if db_field.name == 'hangout':
            		if not request.user.is_superuser:
				get_user = HangoutPermission.objects.filter(access=request.user).values_list('hangout__owner',flat=True)
                		kwargs["queryset"] = Hangout.objects.filter(Q(owner__in=get_user)|Q(owner=request.user))
        	return super(Hangout_ImageGalleryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
                #Limit ImageGallery to those that belong to the request's user.
                qs = super(Hangout_ImageGalleryAdmin, self).queryset(request)
                if request.user.is_superuser:
                        # It is mine, all mine. Just return everything.
                        return qs
		get_user = HangoutPermission.objects.filter(access=request.user)
		owner = []
		for i in get_user:
			owner.append(i.hangout.owner)

                obj = qs.filter(Q(hangout__owner=request.user)|Q(hangout__owner__in=owner))
		return obj"""


class Event_ImageGalleryAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
        	"""Limit choices for 'place' field to only your places."""
        	if db_field.name == 'event':
            		if not request.user.is_superuser:
				get_user = EventPermission.objects.filter(access=request.user).values_list('event__organizer',flat=True)
                		kwargs["queryset"] = Event.objects.filter(Q(organizer__in=get_user)|Q(organizer=request.user))
        	return super(Event_ImageGalleryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
                """Limit ImageGallery to those that belong to the request's user."""
                qs = super(Event_ImageGalleryAdmin, self).queryset(request)
                if request.user.is_superuser:
                        # It is mine, all mine. Just return everything.
                        return qs
		get_user = EventPermission.objects.filter(access=request.user)
		organizer = []
		for i in get_user:
			organizer.append(i.event.organizer)

                obj = qs.filter(Q(event__organizer=request.user)|Q(event__organizer__in=organizer))
		return obj






"""class Hangout_PromotionAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                #Limit choices for 'place' field to only your places.
                if db_field.name == 'hangout':
                        if not request.user.is_superuser:
                                get_user = HangoutPermission.objects.filter(access=request.user).values_list('hangout__owner',flat=True)
                                kwargs["queryset"] = Hangout.objects.filter(Q(owner__in=get_user)|Q(owner=request.user))
                return super(Hangout_PromotionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	

	def get_queryset(self, request):
                #Limit ImageGallery to those that belong to the request's user.    
                qs = super(Hangout_PromotionAdmin, self).queryset(request)
                if request.user.is_superuser:
                        # It is mine, all mine. Just return everything.
                        return qs
                get_user = HangoutPermission.objects.filter(access=request.user)
                owner = []
                for i in get_user:
                        owner.append(i.hangout.owner)

                obj = qs.filter(Q(hangout__owner=request.user)|Q(hangout__owner__in=owner))
                return obj"""



"""class Event_PromotionAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                #Limit choices for 'place' field to only your places.
                if db_field.name == 'event':
                        if not request.user.is_superuser:
                                get_user = EventPermission.objects.filter(access=request.user).values_list('event__organizer',flat=True)
                                kwargs["queryset"] = Event.objects.filter(Q(organizer__in=get_user)|Q(organizer=request.user))
                return super(Promotion_EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	

	def get_queryset(self, request):
                #Limit ImageGallery to those that belong to the request's user.      
                qs = super(Event_PromotionAdmin, self).queryset(request)
                if request.user.is_superuser:
                        # It is mine, all mine. Just return everything.
                        return qs
                get_user = EventPermission.objects.filter(access=request.user)
                organizer = []
                for i in get_user:
                        organizer.append(i.event.organizer)

                obj = qs.filter(Q(event__organizer=request.user)|Q(event__organizer__in=organizer))
                return obj"""


"""class Hangout_StaffAdmin(admin.ModelAdmin):
	form = Hangout_StaffForm

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                
                if db_field.name == 'hangout':
                        if not request.user.is_superuser:
                                get_user = HangoutPermission.objects.filter(access=request.user).values_list('hangout__owner',flat=True)
                                kwargs["queryset"] = Hangout.objects.filter(Q(owner__in=get_user)|Q(owner=request.user))
                return super(Hangout_StaffAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
                     
                qs = super(Hangout_StaffAdmin, self).queryset(request)
                if request.user.is_superuser:
                        # It is mine, all mine. Just return everything.
                        return qs
                get_user = hangoutPermission.objects.filter(access=request.user)
                owner = []
                for i in get_user:
                        owner.append(i.hangout.owner)

                obj = qs.filter(Q(hangout__owner=request.user)|Q(hangout__owner__in=owner))
                return obj
"""



class Event_StaffAdmin(admin.ModelAdmin):
	form = Event_StaffForm

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                """Limit choices for 'place' field to only your places."""
                if db_field.name == 'event':
                        if not request.user.is_superuser:
                                get_user = EventPermission.objects.filter(access=request.user).values_list('event__organizer',flat=True)
                                kwargs["queryset"] = Event.objects.filter(Q(organizer__in=get_user)|Q(organizer=request.user))
                return super(Event_StaffAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
                """Limit ImageGallery to those that belong to the request's user."""            
                qs = super(Event_StaffAdmin, self).queryset(request)
                if request.user.is_superuser:
                        # It is mine, all mine. Just return everything.
                        return qs
                get_user = EventPermission.objects.filter(access=request.user)
                organizer = []
                for i in get_user:
                        organizer.append(i.event.organizer)

                obj = qs.filter(Q(event__organizer=request.user)|Q(event__organizer__in=organizer))
                return obj






"""class HangoutPermissionAdmin(admin.ModelAdmin):

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                
                if db_field.name == 'hangout':
                        if not request.user.is_superuser:
                                kwargs["queryset"] = Hangout.objects.filter(Q(owner=request.user))
                return super(HangoutPermissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



	def save_model(self, request, obj, form, change):
        	if request.user.is_superuser or obj.hangout.owner == request.user:
			pl = Permission.objects.filter(codename__in=["add_hangout_imagegallery", "change_hangout_imagegallery", "delete_hangout_imagegallery","change_hangout","change_hangout_staff","add_hangout_staff","add_hangout_promotion","change_hangout_promotion"])
			obj.access.user_permissions.add(*pl)
            		obj.access.is_staff = True
            		obj.access.save()
			obj.save()

	def get_queryset(self, request):
                qs = super(HangoutPermissionAdmin, self).queryset(request)
                if request.user.is_superuser:
                        return qs
                return qs.filter(Q(hangout__owner=request.user)| Q(access=request.user))

"""


class EventPermissionAdmin(admin.ModelAdmin):

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                """Limit choices for 'place' field to only your places."""
                if db_field.name == 'event':
                        if not request.user.is_superuser:
                                kwargs["queryset"] = Event.objects.filter(Q(organizer=request.user))
                return super(EventPermissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	def save_model(self, request, obj, form, change):
                if request.user.is_superuser or obj.event.organizer == request.user:
                       
			pl = Permission.objects.filter(codename__in=["add_event_imagegallery", "change_event_imagegallery", "delete_event_imagegallery","change_event","change_event_staff","add_event_staff","add_event_promotion","change_event_promotion"])
                        obj.access.user_permissions.add(*pl)
                        obj.access.is_staff = True
                        obj.access.save()
                        obj.save()

	def get_queryset(self, request):
                qs = super(EventPermissionAdmin, self).queryset(request)
                if request.user.is_superuser:
                        return qs
                return qs.filter(Q(event__organizer=request.user)| Q(access=request.user))


class ProfileLimitationAdmin(admin.ModelAdmin):
	pass

class UserProfileAdmin(admin.ModelAdmin):
	def get_query_set(self):
        	qs = super(UserProfileAdmin, self).get_query_set()
        	return qs.distinct()







class UserStatusAdmin(admin.ModelAdmin):
	pass


#class Hangout_LikedAdmin(admin.ModelAdmin):
#	pass

class Event_LikedAdmin(admin.ModelAdmin):
	pass

class Upload_ImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

class User_ConnectionAdmin(admin.ModelAdmin):
	pass

class User_Details_EarlierAdmin(admin.ModelAdmin):
	pass

class User_DetailsAdmin(admin.ModelAdmin):
	pass

class EventPermissionAdmin(admin.ModelAdmin):
	pass

class Event_CommentAdmin(admin.ModelAdmin):
	pass


class SimilarEventAdmin(admin.ModelAdmin):
	search_fields = ['event__tags']
	
	"""def get_queryset(self,request):
		qs = super(SimilarArticleAdmin,self).get_queryset(request)
		article_id = request.GET.get('ids',None)
		if article_id != None:
			article_obj = Article.objects.get(id=article_id)
			similar_obj = SimilarArticle.objects.get_or_create(article=article_obj)
			#similar_obj.save()
			print "similar"
			#return HttpResponseRedirect('/admin/article/article/?e=2')
		print "article_id",article_id
		#print "similar",similar_obj
		return qs"""


admin.site.register(SimilarEvent,SimilarEventAdmin)
admin.site.register(Upload_Image, Upload_ImageAdmin)
admin.site.register(Event_Liked,Event_LikedAdmin)
#admin.site.register(Hangout_Liked,Hangout_LikedAdmin)
admin.site.register(UserStatus,UserStatusAdmin)
admin.site.register(User_Connection,User_ConnectionAdmin)
admin.site.register(UserProfile,UserProfileAdmin)	
admin.site.register(ProfileLimitation,ProfileLimitationAdmin)
#admin.site.register(EventPermission,EventPermissionAdmin)
#admin.site.register(HangoutPermission,HangoutPermissionAdmin)
#admin.site.register(Hangout_Promotion,Hangout_PromotionAdmin)
#admin.site.register(Hangout_Staff,Hangout_StaffAdmin)
#admin.site.register(Hangout_ImageGallery,Hangout_ImageGalleryAdmin)
#admin.site.register(Event_Promotion,Event_PromotionAdmin)
admin.site.register(Event_Staff,Event_StaffAdmin)
admin.site.register(Event_ImageGallery,Event_ImageGalleryAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Hangout,HangoutAdmin)
admin.site.register(User_Details_Earlier,User_Details_EarlierAdmin)
admin.site.register(User_Details,User_DetailsAdmin)
admin.site.register(EventPermission,EventPermissionAdmin)
admin.site.register(Event_Comment,Event_CommentAdmin)
