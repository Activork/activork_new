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
    url(r'^$', 'django_social_app.views.login'),
    url(r'^home/$', 'django_social_app.views.home'),
    url(r'^logout/$', 'django_social_app.views.logout'),
    url(r'^self_profile/$','myapp.views.self_profile',name='self_profile'),
    url(r'^settings/$','myapp.views.settings',name='settings'),
    url(r'^messages/$','myapp.views.messages',name='messages'),
    url(r'^notifications/$','myapp.views.notifications',name='notifications'),
    url(r'^mobile/signup/$','django_social_app.views.mobile_signup',name='mobile_signup'),
    url(r'^mobile/login/$','django_social_app.views.mobile_login',name='mobile_login'),
   
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
