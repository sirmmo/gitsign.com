# Create your views here.
from tasks import *
from django.http import HttpResponse

def upadte_repos(request):
	username = request.REQUEST.get('username', request.user.username)
	load_user.delay(username)
	load_repos.delay(username)
	return HttpResponse()