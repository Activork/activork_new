from django.contrib import admin
from .models import SimilarArticle,Article
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

"""def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    print admin.ACTION_CHECKBOX_NAME
    print selected
    print queryset.model
    #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    return HttpResponseRedirect("/export/article/?ct=%s&ids=%s"%(ct.pk,",".join(selected)))"""

class ArticleAdmin(admin.ModelAdmin):
	search_fields = ['name']
	actions = ['export_selected_objects']


	def export_selected_objects(self, request, queryset):
                selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                ct = ContentType.objects.get_for_model(queryset.model)
                print admin.ACTION_CHECKBOX_NAME
                print selected
                print queryset.model
                #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
                return HttpResponseRedirect("/export/article/?ct=%s&ids=%s"%(ct.pk,",".join(selected)))

	"""def get_queryset(self,request):
		qs = super(ArticleAdmin,self).get_queryset(request)
		previous = request.GET.get('ids',None)
		print "previous",previous
		return qs"""


	def get_queryset(self,request):
                qs = super(ArticleAdmin,self).get_queryset(request)
                article_id = request.GET.get('ids',None)
                if article_id != None:
                        article_obj = Article.objects.get(id=article_id)
                        similar_obj = SimilarArticle.objects.get_or_create(article=article_obj)
                        #similar_obj.save()
                        print "similar"
                        #return HttpResponseRedirect('/admin/article/article/?e=2')
                print "article_id",article_id
                #print "similar",similar_obj
                return qs



class SimilarArticleAdmin(admin.ModelAdmin):
	search_fields = ['article__tags']
	
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

admin.site.register(Article,ArticleAdmin)
admin.site.register(SimilarArticle,SimilarArticleAdmin)
