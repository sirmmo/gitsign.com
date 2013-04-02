from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from pprint import pprint
from core.models import *
from core.views import *

import json
from datetime import datetime

def index (request):
	ctx = {}
	if request.user.is_authenticated():
		ctx['loggedin'] = True
		ctx['username'] = request.user.username
	else:
		ctx['loggedin'] = False
	ctx['signs'] = Sign.objects.count()
	ctx['users'] = UserData.objects.count()
	ctx['repos'] = Repo.objects.count()
	ctx['latest_users'] = UserData.objects.all().order_by('?')[:10]

	return render_to_response('index.html', ctx)


def profile(request, username, sign=None):


	if User.objects.filter(username = username).count() == 0:
		return HttpResponseRedirect('/')
	editable = request.user.username == username
	repos = Repo.objects.filter(starred_by__user__username = username)
	if sign is not None:
		repos = repos.filter(signed__sign__slug=sign)
	#repos = Repo.objects.all()
	#raise Exception()

	ctx = {
		'editable':editable,
		'user':User.objects.get(username =username), 
		'user_profile':UserData.objects.get(user__username=username), 
		'repos':repos, 
	}
	if sign is not None:
		ctx['sign'] = sign
	if request.user.is_authenticated():
		ctx['loggedin'] = True
		ctx['username'] = request.user.username
	else:
		ctx['loggedin'] = False

	return render_to_response('profile.html', ctx )

def loading(request):
	username = request.user.username
	load_user(username)
	load_repos.delay(username)
	return HttpResponseRedirect("/")

def signs(request, username):
	#.values('id', 'name', 'slug', 'color')
	prep = [x for x in Sign.objects.filter(owner__username = username)]
	ret = []
	for x in prep :
		ret.append({
			'id':x.id,
			'color':x.color,
			'name':x.name,
			'slug':x.slug,
			'amount':x.amount
		})
	return HttpResponse(json.dumps(ret ))

def repos(request, username, sign=None):
	page = int(request.REQUEST.get('page', '1'))
	amount = 30
	start = (page-1)*amount
	end = page*amount
	repos_origin = Repo.objects.filter(starred_by__user__username = username)
	if sign is not None:
		repos_origin = repos_origin.filter(signed__sign__slug = sign)
	reps = [x for x in repos_origin 
		.values("last_update", "id", "name", "owner", "owner_type", "remote", "page", "is_fork", "created", "updated", "forks", "watchers")]#[start:end]]
	reps_new = []
	for repo in reps:
		repo['created'] = datetime.strftime(repo['created'], '%b %d, %Y, %I:%M %p')
		repo['updated'] = datetime.strftime(repo['updated'], '%b %d, %Y, %I:%M %p')
		repo['last_update'] = datetime.strftime(repo['last_update'], '%b %d, %Y, %I:%M %p')
		repo['signs'] = [{
			'sid':x.id,
			'color':x.color,
			'name':x.name,
			'slug':x.slug,
			'rid':repo['id']
		} for x in Sign.objects.filter(owner__username=username, stars__repo__id = repo['id'])]
		reps_new.append(repo)
	return HttpResponse(json.dumps(reps_new ))

def unsign(request, username):
	sid = request.REQUEST.get('sid')
	rid = request.REQUEST.get('rid')

	if sid is None or rid is None:
		return HttpResponse('fail')
	

	RS.objects.get(repo__id = rid, sign__id = sid, user__username =username).delete()
	return HttpResponse(200)
