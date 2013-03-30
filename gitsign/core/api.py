from tastypie.resources import ModelResource
from core.models import *
from tastypie.api import Api

gitsign_api = Api(api_name='stargaze')


class SignResource(ModelResource):
	class Meta:
		queryset = Sign.objects.all()
		resource_name = "sign"

class RepoResource(ModelResource):
	class Meta:
		queryset = Repo.objects.all()
		resource_name = "repo"

class RSResource(ModelResource):
	class Meta:
		queryset = RS.objects.all()
		resource_name = "reposign"

gitsign_api.register(SignResource())
gitsign_api.register(RepoResource())
gitsign_api.register(RSResource())