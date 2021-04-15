from django.contrib import admin

# Register your models here.
from .models import chatlits, Message
admin.site.register(chatlits)
admin.site.register(Message)