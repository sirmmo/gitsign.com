import celery

from core.models import *

@celery.task
def load_repos(username):
	
