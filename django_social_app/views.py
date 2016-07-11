from django.shortcuts import render
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from notifications.signals import notify
from .models import MyUser
from allauth.account.views import SignupView, LoginView
from allauth.account.forms import LoginForm, SignupForm

from allauth.account.utils import (get_next_redirect_url, complete_signup,
                    get_login_redirect_url, perform_login,
                    passthrough_next_redirect_url, url_str_to_user_pk,
                    logout_on_password_change)

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import (HttpResponseRedirect, Http404,
                         HttpResponsePermanentRedirect)
from rest_framework.decorators import api_view
from rest_framework.response import Response

#api serializers
from .models import MyUserSerializer




@api_view(['GET','POST'])
def mobile_signup(request):
	if request.method == "GET":
		user = MyUser.objects.all()
		serializer = MyUserSerializer(user,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		serializer = MyUserSerializer(data=request.data)
		if serializer.is_valid():
			username = request.data["username"]
			first_name = username
			email = request.data["email"]	
			phone_no = request.data["phone_no"]
			password = request.data["password"]
			user = MyUser(username=username,first_name=first_name,email=email,phone_no=phone_no,password=password)
			user.set_password(user.password)
			user.save()
		else:
			return Response(serializer.errors)


		serializer = MyUserSerializer(user)
		return Response({'user_data':serializer.data,'SESSION_ID':request.session.session_key})



@api_view(['POST'])
def mobile_login(request):
	if request.method == "POST":
		email = request.data["email"]
		password = request.data["password"]
		user = auth.authenticate(email=email,password=password)


		if user:
			if user.is_active:
				auth.login(request,user)
				serializer = MyUserSerializer(user)
				return Response({'user_data':serializer.data,'SESSION_ID':request.session.session_key})
			else:
				return Response("please verify your email")

		else:
			return Response("Invlaid Credentials")

	else:
		return Response("Get Request")


class MySignupView(SignupView):
    template_name = 'my_signup.html'
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret

    def form_valid(self, form):
        user = form.save(self.request)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_context_data(self, **kwargs):
        form = kwargs['form']
        form.fields["email"].initial = self.request.session \
            .get('account_verified_email', None)
        ret = super(SignupView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value,"login_form":LoginForm()})
        return ret

class MyLoginView(LoginView):
    template_name = 'my_signup.html'
    form_class = LoginForm
    #template_name = "account/signup.html"
    success_url = None
    redirect_field_name = "next"

    def form_valid(self, form):
        success_url = self.get_success_url()
        return form.login(self.request, redirect_url=success_url)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
	ret['login_form']= ret['form']
	ret['form'] = SignupForm()
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("account_signup"),
                                                   self.redirect_field_name)
        redirect_field_value = self.request.REQUEST \
            .get(self.redirect_field_name)
        ret.update({"signup_url": signup_url,
                    "site": Site.objects.get_current(),
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

def login(request):
    return render(request,'login.html')


@login_required(login_url='/')
def home(request):
    notify.send(MyUser.objects.get(id=3), recipient=request.user, action_object=MyUser.objects.get(id=1), verb='you reached level 10')
    return render(request,'home.html')


def logout(request):
    auth_logout(request)
    return redirect('/accounts/signup/')
