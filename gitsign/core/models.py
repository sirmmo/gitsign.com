from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Sign(models.Model):
	owner = models.ForeignKey(User)
	name=models.CharField(max_length=400)
	slug=models.SlugField(null=True, blank=True)
	color = models.CharField(max_length=6, default="119BAC")

	class Meta:
		ordering =['name']

	@property
	def amount(self):
		return self.stars.all().count()

	def save(self, *args, **kwargs):
		self.slug = slugify (self.name)
		super(Sign,self ).save(args, kwargs)

class Repo(models.Model):
	last_update = models.DateTimeField(auto_now=True)
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
	def __str__(self):
		return self.name

	class Meta:
		ordering =['name']


class Star(models.Model):
	user = models.ForeignKey(User, related_name="starred")
	repo = models.ForeignKey(Repo, related_name="starred_by")

	class Meta:
		unique_together = ['user','repo']

class RS(models.Model):
	repo = models.ForeignKey(Repo, related_name="signed")
	sign = models.ForeignKey(Sign, related_name="stars")
	user = models.ForeignKey(User)
	note = models.TextField(default="")

	class Meta:
		unique_together = ['repo', 'sign']

class UserData(models.Model):
	user = models.ForeignKey(User, related_name="user_profile", unique=True)
	avatar = models.URLField(default="")
	name = models.TextField(null=True, blank=True, default="")
	type = models.TextField()
	url = models.URLField()

	def __str__(self):
		return self.user.username