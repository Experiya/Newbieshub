from django.shortcuts import render
from django.urls import path
from .import views

urlpatterns = [
    path('',views.homeFreelancer,name='homeFreelancer'),
    path('signUp',views.signUp,name='signUp'),
    path('signIn',views.signIn,name='signIn'),
    path('signOut',views.signOut,name='signOut'),
    #path('secondStageImageUpdate',views.secondStageImageUpdate,name='secondStageImageUpdate'),
    path('myProfile',views.myProfile,name='myProfile'),
    path('updateProfile/<int:edit_id>', views.updateProfile,name='updateProfile'),
    path('myGig',views.myGig,name='myGig'),
    path('editGig/<int:edit>',views.editGig,name='editGig'),
    path('deleteGig/<int:delete_id>', views.deleteGig,name='deleteGig'),
    path('testExam',views.testExam,name='testExam'),
    path('save_ans',views.save_ans,name="saveans"),
    path('result',views.result,name='result'),
    path('displayRequests',views.displayRequests,name='displayRequests'),
    path('acceptRequest',views.acceptRequest,name='acceptRequest'),
    path('chat',views.chat,name='chat'),
    path('public',views.public,name='public'),
    path("qvProject/<int:myid>", views.qvProject, name="qvProject"),
    path('MyTimeline',views.MyTimeline,name='MyTimeline'),
    path("viewTimeline/<int:x>", views.viewTimeline, name="viewTimeline"),
    path('staticChat', views.staticChat, name="staticChat"),
    path('uploadFiles/<int:t>', views.uploadFiles, name="uploadFiles"),
    path('makeReport/<int:z>',views.makeReport,name='makeReport')
]