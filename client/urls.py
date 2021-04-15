from django.shortcuts import render
from django.urls import path
from .import views
urlpatterns = [
    path('',views.homeClient,name='homeClient'),
    path('signUp',views.signUp,name='signUp'),
    path('signIn',views.signIn,name='signIn'),
    path('signOut',views.signOut,name='signOut'),
    path('myProfile',views.myProfile,name='myProfile'),
    path('myProject',views.myProject,name='myProject'),
    path('updateProfile/<int:edit_id>', views.updateProfile,name='updateProfile'),
    path('deleteProject/<int:delete_id>', views.deleteProject,name='deleteProject'),
    path('updateProject/<int:update_id>',views.updateProject,name='updateProject'),
    path('public',views.public,name='public'),
    path("qvFreelancer/<int:myid>", views.qvFreelancer, name="qvFreelancer"),
    path('chat',views.chat,name='chat'),
    path('displayRequests',views.displayRequests,name='displayRequests'),
    path('acceptRequest',views.acceptRequest,name='acceptRequest'),
    path('MyTimeline',views.MyTimeline,name='MyTimeline'),
    path("viewTimeline/<int:x>", views.viewTimeline, name="viewTimeline"),
    path('uploadFiles/<int:t>', views.uploadFiles, name="uploadFiles"),
    path('payment/<int:u>', views.payment, name="payment"),
    path('giveReviews/<int:v>', views.giveReviews, name="giveReviews"),
    path('makeReport/<int:z>',views.makeReport,name='makeReport')
]