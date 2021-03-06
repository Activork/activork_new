from datetime import timedelta
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from notifications.signals import notify
from .models import MyUser
from allauth.account.views import SignupView, LoginView
from allauth.account.models import EmailAddress
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required

from allauth.account.utils import (get_next_redirect_url, complete_signup,
                    get_login_redirect_url, perform_login,
                    passthrough_next_redirect_url, url_str_to_user_pk,
                    logout_on_password_change)

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import (HttpResponseRedirect, Http404,
                         HttpResponsePermanentRedirect)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import load_backend, login
from django.conf import settings

#api serializers
from .models import MyUserSerializer
from django.contrib import auth
from django.core.mail import send_mail
#from django.contrib.auth.decorators import get_user_object


def get_user_object(fun):
        def get_user(request,*args,**kwargs):
                session_key = request.META['HTTP_SESSION_ID']

		print session_key

                session = Session.objects.get(session_key=session_key)
                user_id = session.get_decoded().get('_auth_user_id')
                request.user = MyUser.objects.get(pk=user_id)

                return fun(request,*args,**kwargs)
        return get_user




@api_view(['POST'])
def mobile_social_signup(request):
	if request.method == "POST":
		username = request.data["username"]
		if MyUser.objects.filter(username=username).exists():
			username = username + request.data["uid"]
		else:
			username = username
		first_name = username
		email = request.data["email"]
		user = MyUser(username=username,first_name=first_name,email=email,is_active = True, is_staff=False,is_superuser=False,phone_no = "")
		user.save()

		uid = request.data["uid"] 
		provider = request.data["provider"]
		extra_data = request.data["ectra_data"]

		social_obj = SocialAccount(user=user,provider=provider,uid=uid,extra_data=extra_data)
		social_obj.save()

	else:
		user = User.objects.get(username = request.data["username"])

	if not hasattr(user,'backend'):
		for backend in settings.AUTHENTICATION_BACKENDS:
			if user == load_backend(backend).get_user(user.pk):
				user.backend= backend
				break
	if hasattr(user,'backend'):
		login(request,user)


	serializer = MyUserSerializer(user)
	return Response({'user_data':serializer.data,'SESSION_ID':reuest.session.session_key})	
					


@api_view(['POST'])
@get_user_object
def mobile_change_password(request):
	if request.method == "POST":
		user = request.user	
		if user:
			new_password = request.data['new_password']
			user.set_password(new_password)
			user.save()
			return Response("Changed Sucessfully")

		else:
			return Response("please login")


@api_view(['POST','GET'])
def mobile_forgot_password(request):
	print request.method
	if request.method == "POST":
		
		email = request.data['email']
		print type(email)
		user_check = MyUser.objects.filter(email=email).exists()
		if not user_check:
			return Response("No user exists with this email")

		else:
			user = MyUser.objects.get(email=email)
			print user
			
			send_mail('Forgot Password',"Change your password https://activork-new.herokuapp.com/mobile/reset_password/?user="+str(user.id)+"",'metawing30@gmail.com',[str(email)])
			
		return Response("Please follow the link sent on your registered email id")
	
	if request.method == "GET":
		return Response("GET")
		

@api_view(['POST'])
def mobile_reset_password(request):
	if request.method == "POST":
		password1 = request.data['password1']
		password2 = request.data['password2']


		if password1 != password2:
			return Response("Passwords do not match")

		else:
			user_id = request.GET.get('user',"Not exists")
			
			#return Response(user_id)

			print "user",user_id

			try:
				user_id = int(user_id)

			except:
				user_id = None


			print "user",user_id


			if user_id != None:
				check = MyUser.objects.filter(id=user_id).exists()

				if check:
					user_obj = MyUser.objects.get(id=user_id)
					user_obj.set_password(password1)
					user_obj.save()
					print user_obj.password
					return Response("password changes sucessfully")
				else:
					return Response("No user exists with this email id")
			else:
				return Response("Unsufficient data")


def send_email_confirmation(request, user, signup=False):
    """
    E-mail verification mails are sent:
    a) Explicitly: when a user signs up
    b) Implicitly: when a user attempts to log in using an unverified
    e-mail while EMAIL_VERIFICATION is mandatory.

    Especially in case of b), we want to limit the number of mails
    sent (consider a user retrying a few times), which is why there is
    a cooldown period before sending a new mail.
    """
    from allauth.account.models import EmailAddress, EmailConfirmation

    COOLDOWN_PERIOD = timedelta(minutes=3)
    email = user.email
    if email:
        try:
            email_address = EmailAddress.objects.get_for_user(user, email)
            if not email_address.verified:
                send_email = not EmailConfirmation.objects \
                    .filter(sent__gt=now() - COOLDOWN_PERIOD,
                            email_address=email_address) \
                    .exists()
                if send_email:
                    email_address.send_confirmation(request,
                                                    signup=signup)
            else:
                send_email = False
        except EmailAddress.DoesNotExist:
            send_email = True
            email_address = EmailAddress.objects.add_email(request,
                                                           user,
                                                           email,
                                                           signup=signup,
                                                           confirm=True)
            #assert email_addresspi_view(['GET','POST'])

	return




from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
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
			check_username = MyUser.objects.filter(username=username).exists()
			if check_username:
				return Response("Username Already Exists, Please enter anothe one")	

			check_email = MyUser.objects.filter(email=email).exists()
			if check_email:
				return Response("Email Already Exists")

			phone_no = request.data["phone_no"]
			password = request.data["password"]
			user = MyUser(username=username,first_name=first_name,email=email,phone_no=phone_no,password=password)
			user.set_password(user.password)
			user.save()

			#session_id = request.session._get_or_create_session_key()

			request.session.modified = True
		
			session_id = request.session._session_key

			print session_id

			send_email_confirmation(request, user, signup=True)
		else:
			return Response(serializer.errors)


		serializer = MyUserSerializer(user)
		return Response({'user_data':serializer.data,'SESSION_ID':session_id})



@api_view(['POST','GET'])
def mobile_login(request):
	#print request.method
	#print request.data
	if request.method == "POST":
		print "in"
		email = request.data["email"]
		password = request.data["password"]
		print email,password
		user = auth.authenticate(email=email,password=password)

		print user

		print request.session._session_key

		if user:

			has_verified_email = EmailAddress.objects.filter(user=user,verified=True).exists()


                	if not has_verified_email:
                        	return Response("please verify your email")


			if user.is_active:
				auth.login(request,user)
				serializer = MyUserSerializer(user)
				return Response({'user_data':serializer.data,'SESSION_ID':request.session._session_key})
			else:
				return Response("your account is not active")

		else:
			return Response("Invlaid Credentials")

	if request.method == "GET":
		return Response("in GET")


@api_view(['POST'])
def mobile_logout(request):
	auth_logout(request)
	return Response("Logged out")




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
    #send_mail('ada','dd','metawing30@gmail.com',['pdpreetidewani188@gmail.com'])
    return render(request,'login.html')


@login_required(login_url='/')
def home(request):
    notify.send(MyUser.objects.get(id=3), recipient=request.user, action_object=MyUser.objects.get(id=1), verb='you reached level 10')
    return render(request,'home.html')


def logout(request):
    auth_logout(request)
    return redirect('/accounts/signup/')
