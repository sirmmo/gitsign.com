import celery
from django.conf import settings
from core.models import *

import requests
import json

@celery.task
def load_user(username):
	print 'update ', username
	r = requests.get('https://api.github.com/users/%s' % username ,params={"client_id":settings.GITHUB_APP_ID, "client_secret":settings.GITHUB_API_SECRET})
	d = r.json()
	print d
	if UserData.objects.filter(user__username = username).count() > 0:
		u = UserData.objects.get(user__username = username)
	else:
		u = UserData()
		u.user = User.objects.get(username = username)
	u.avatar = d['avatar_url']
	if 'name' in d:
		u.name = d['name']
	u.type = d['type']
	u.url = d['html_url']
	u.save()


@celery.task
def load_repos(username):
	last = False
	page = 1
	while not last:
		r = requests.get('https://api.github.com/users/%s/starred' % username, params={'page':page,"client_id":settings.GITHUB_APP_ID, "client_secret":settings.GITHUB_API_SECRET})
		#print r.url
		page += 1
		if r.status_code == 200:
			m = r.json()
			if len(m) < 30:
				last = True
			for repo in m:
				save_repo.delay(repo, username)	

@celery.task
def save_repo(data, username):
	print 'adding repo '+ str(data['id'])
	try:
		repo = Repo.objects.get(id=data['id'])
		dd = datetime.datetime.now() - repo.last_update
		if dd.days < 1:
			return
	except:
		repo = Repo()
		repo.id = data['id']
		repo.remote = ""
	repo.name = data["full_name"]
	repo.owner = data['owner']['login']
	repo.owner_type = data['owner']['type']
	repo.page = data["html_url"]
	repo.is_fork = data["fork"]
	repo.created = data["created_at"]
	repo.updated = data["updated_at"]
	repo.forks = data["forks_count"]
	repo.watchers = data["watchers_count"]	
	repo.save()
	#print "saved repo, starring"
	star_repo.delay(repo.id, username)

@celery.task
def star_repo(repo_id, username):
	try:
		#print "star"
		s = Star()
		#print "data"
		s.user = User.objects.get(username = username)
		s.repo = Repo.objects.get(id=repo_id)
		#print "save"
		s.save()
	except:
		#print "fail"
		pass

