from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from notifications.signals import notify
from .models import MyUser
from allauth.account.views import SignupView, LoginView


class MySignupView(SignupView):
    template_name = 'my_signup.html'


class MyLoginView(LoginView):
    template_name = 'my_login.html'

def login(request):
    return render(request,'login.html')


@login_required(login_url='/')
def home(request):
    notify.send(MyUser.objects.get(id=3), recipient=request.user, action_object=MyUser.objects.get(id=1), verb='you reached level 10')
    return render(request,'home.html')


def logout(request):
    auth_logout(request)
    return redirect('/accounts/signup/')
