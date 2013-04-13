from tastypie.resources import ModelResource
from core.models import *
from tastypie.api import Api
from tastypie.authorization import DjangoAuthorization, Authorization
import json

gitsign_api = Api(api_name='stargaze')


class SignResource(ModelResource):
	class Meta:
		queryset = Sign.objects.all()
		resource_name = "sign"

		authorization = Authorization()

	def obj_create(self, bundle, **kwargs):		
		return super(SignResource, self).obj_create(bundle, owner =bundle.request.user)

class RepoResource(ModelResource):
	class Meta:
		queryset = Repo.objects.all()
		resource_name = "repo"

		authorization = Authorization()

class RSResource(ModelResource):
	class Meta:
		queryset = RS.objects.all()
		resource_name = "reposign"
		authorization = Authorization()
	def obj_create(self, bundle, **kwargs):	
		data = bundle.request.body
		data = json.loads(data)
		repo = Repo.objects.get(id=data.get('repo'))
		sign = Sign.objects.get(id=data.get('sign'))
		return super(RSResource, self).obj_create(bundle, user =bundle.request.user, repo = repo, sign=sign)



gitsign_api.register(SignResource())
gitsign_api.register(RepoResource())
gitsign_api.register(RSResource())