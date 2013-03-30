from django.db import models
from django.contrib.auth.models import User

class Sign(models.Model):
	owner = models.ForeignKey(User)
	name=models.CharField(max_length=400)
	color = models.CharField(max_length=6, default="119BAC")

class Repo(models.Model):
	id = models.IntegerField(unique=True, primary_key=True)
	name = models.TextField()
	owner = models.TextField()
	owner_type = models.TextField()
	remote = models.URLField()
	page = models.URLField()
	is_fork = models.BooleanField()
	created = models.DateTimeField()
	updated = models.DateTimeField()
	forks = models.IntegerField()
	watchers = models.IntegerField()

class Star(models.Model):
	user = models.ForeignKey(User)
	repo = models.ForeignKey(Repo)

class RS(models.Model):
	repo = models.ForeignKey(Repo)
	sign = models.ForeignKey(Sign)
	user = models.ForeignKey(User)
	note = models.TextField()