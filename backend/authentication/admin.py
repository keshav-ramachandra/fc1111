from django.contrib import admin
from authentication.models import User
from authentication.models import FreemiumUser
# Register your models here.

admin.site.register(User)
admin.site.register(FreemiumUser)