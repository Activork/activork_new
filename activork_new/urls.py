from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django_social_app.views import MySignupView,MyLoginView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'main_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/signup/$', MySignupView.as_view(template_name="my_signup.html")),
    url(r'^accounts/login/$',MyLoginView.as_view()),
    url(r'^accounts/', include('allauth.urls')),


#django_social_app urls

    url(r'^$', 'django_social_app.views.login'),
    url(r'^home/$', 'django_social_app.views.home'),
    url(r'^logout/$', 'django_social_app.views.logout'),

#myapp urls


    url(r'^home_page/$','myapp.views.home_page',name='home_page'),
    url(r'^self_profile/$','myapp.views.self_profile',name='self_profile'),
    url(r'^settings/$','myapp.views.settings',name='settings'),
    url(r'^messages/$','myapp.views.messages',name='messages'),
    url(r'^notifications/$','myapp.views.notifications',name='notifications'),
    url(r'^export/event/$','myapp.views.export_event',name='export_event'),
    url(r'^save_similar_event/$','myapp.views.save_similar_event',name='similar_event'),
    url(r'^update_status/$','myapp.views.update_status',name='update_status'),
    url(r'^get_details/$','myapp.views.get_details',name='get_details'),
    url(r'^like_event/$','myapp.views.like_event',name='like_event'),
    url(r'^comment_on_event/$','myapp.views.comment_on_event',name='comment_on_event'),
    url(r'^going_event/$','myapp.views.going_event',name='going_event'),
    #url(r'^event_page/(?P<event_id>\d+)/$','myapp.views.event_page',name='event_page'),


#article urls

    
    url(r'^article_home/$','article.views.home',name='home'),
    url(r'^article_page/(?P<article_id>\d+)/$','article.views.article_page',name='article_page'),
    url(r'^update_time/$','article.views.update_time',name='update_time'),
    url(r'^export/article/$','article.views.export_article',name='export_article'),
    url(r'^save_similar_article/$','article.views.save_similar_article'),
    url(r'^like_article/$','article.views.like_article',name='like_event'),
    url(r'^comment_on_article/$','article.views.comment_on_article',name='comment_on_article'),
    url(r'^rate_article/$','article.views.rate_article',name='rate_article'),
   
#app urls


    url(r'^mobile/signup/$','django_social_app.views.mobile_signup',name='mobile_signup'),
    url(r'^mobile/login/$','django_social_app.views.mobile_login',name='mobile_login'),
    url(r'^mobile/logout/$','django_social_app.views.mobile_logout',name='mobile_logout'),
    url(r'^mobile/social_signup/$','django_social_app.views.mobile_social_signup',name='mobile_social_signup'),
    url(r'^mobile/change_password/$','django_social_app.views.mobile_change_password',name='mobile_change_password'),
    url(r'^mobile/forgot_password/$','django_social_app.views.mobile_forgot_password'),
    url(r'^mobile/reset_password/$','django_social_app.views.mobile_reset_password'),
    url(r'^mobile/get_details/$','myapp.views.mobile_get_details',name='mobile_get_data'),
    url(r'^mobile/home_page/$','myapp.views.mobile_home_page',name='mobile_home_page'),
    url(r'^mobile/update_status/$','myapp.views.mobile_update_status',name='mobile_update_status'),
    url(r'^mobile/like_event/$','myapp.views.mobile_like_event',name='mobile_like_event'),
    url(r'^mobile/like_article/$','myapp.views.mobile_like_article',name='mobile_like_article'),
    url(r'^mobile/comment_on_event/$','myapp.views.mobile_comment_on_event',name='mobile_comment_on_event'),
    url(r'^mobile/comment_on_article/$','myapp.views.mobile_comment_on_article',name='mobile_comment_on_article'),
    url(r'^mobile/going_event/$','myapp.views.mobile_going_event',name='mobile_going_event'),
    #url(r'^mobile/event_page/(?P<event_id>\d+)/$','myapp.views.mobile_event_page',name='mobile_event_page'),
    url(r'^mobile/article_page/(?P<article_id>\d+)/$','myapp.views.mobile_article_page'),
    url(r'^mobile/rate_article/$','myapp.views.mobile_rate_article',name='mobile_rate_article'),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
