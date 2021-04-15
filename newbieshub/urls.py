from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('events/',views.events,name='events'),
    path('freelancer/',include('freelancer.urls')),
    path('client/',include('client.urls')),
    path('chat/',include('chat.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
