from django.contrib import admin

# Register your models here.
from .models import client,requestByClient
admin.site.register(client)
admin.site.register(requestByClient)
from .models import project
admin.site.register(project)