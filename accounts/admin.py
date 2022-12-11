from django.contrib import admin

from accounts.models import CustomUser, Hit

admin.site.register(CustomUser)
admin.site.register(Hit)

