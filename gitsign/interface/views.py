from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from pprint import pprint
def index (request):
	return render_to_response('index.html')


def profile(request):
	instance = UserSocialAuth.objects.filter(provider='github').get(user=User.objects.get(username=request.user.username))

	return render_to_response('profile.html', {'user':request.user})