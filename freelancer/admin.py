from django.contrib import admin

# Register your models here.
from .models import freelancer,test, requestByFreelancer, timelineFC, trashFiles, report
admin.site.register(freelancer)
admin.site.register(requestByFreelancer)
admin.site.register(test)
from .models import gig
admin.site.register(gig)
admin.site.register(timelineFC)
admin.site.register(trashFiles)
admin.site.register(report)