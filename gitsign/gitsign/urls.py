from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.api import gitsign_api

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'interface.views.index', name='home'),
    url(r'', include('social_auth.urls')),

    url(r'^update', 'core.views.upadte_repos', name="update"),
    url(r'^api/', include(gitsign_api.urls)),
    url(r'^loading', 'interface.views.loading'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^u/(?P<username>\w+)$', 'interface.views.profile', name="profile"),
    url(r'^u/(?P<username>\w+)/j/signs$', 'interface.views.signs', name="signs"),
    url(r'^u/(?P<username>\w+)/j/repos$', 'interface.views.repos', name="repos"),
    url(r'^u/(?P<username>\w+)/j/repos/(?P<sign>[\w-]+)$', 'interface.views.repos', name="repos"),
    url(r'^u/(?P<username>\w+)/o/unsign$', 'interface.views.unsign', name="remove"),
    url(r'^u/(?P<username>\w+)/(?P<sign>[\w-]+)', 'interface.views.profile', name="sign"),
)
