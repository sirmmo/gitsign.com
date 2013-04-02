from django.contrib import admin

from core.models import *

admin.site.register(Repo)
admin.site.register(Star)
admin.site.register(Sign)
admin.site.register(UserData)