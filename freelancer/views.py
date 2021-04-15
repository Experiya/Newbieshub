from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from math import ceil
import datetime
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import freelancer, gig,test, requestByFreelancer, timelineFC, trashFiles, report
from chat.models import chatlits
from client.models import requestByClient,project, client
from django.db import models
import json
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from PIL import Image




def homeFreelancer(request):
  loginStatus = request.session.get('login')
  if loginStatus == 'yes':
    name = request.session.get('mainName')
    params={'name':name}
    return render(request,'freelancer/index.html',params)
  else:
    return render(request,'freelancer/index.html')


def signUp(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if len(username)>16:
            messages.error(request, " Your user name must be under 15 characters")
            return redirect('homeFreelancer')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('homeFreelancer')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('homeFreelancer')
        try:
          temp = freelancer(username=username,name=name,email=email,password=pass1,rating=0,levels="primary",category="",sub_category="",date=datetime.datetime.now(),image="/freelancer/images/dp.png")
          temp.save()
          messages.success(request, " Your account has been successfully created")
          return redirect('homeFreelancer')
        except IntegrityError as e:
          if 'UNIQUE constraint failed' in e.args[0]:
            messages.warning(request, "This name and email-id Exists already!. Please choose a unique name")
            return redirect('homeFreelancer')

    else:
        messages.warning(request, "404 - Not found | Something goes wrong ")
        return redirect('homeFreelancer')


def authentication(request,credential):
  data= freelancer.objects.all()
  count = 0
  for i in data:
    if ((i.username == credential["username"]) and (i.password == credential["password"])):
      count = 1
      a=freelancer.objects.get(username=credential["username"])
      params={'name':credential["username"],'id':a.id,"count":"1"}
      request.session['mainName']= credential["username"]
      request.session['mainPass']= credential["password"]
      request.session['mainId'] = a.id
      request.session['mainReview'] = a.rating
      request.session['login'] = 'yes'
      return params
      break
  if count==0:
    params={"count":"0"}
    return params


def signIn(request):
    data= freelancer.objects.all()
    if request.method=='POST':
      username = request.POST['loginusername']
      password = request.POST['loginpassword']
      credential={"username":username,"password":password}
      params = authentication(request,credential)
      if params['count']=="1":
        messages.success(request, "Successfully Logged In")
        #return render(request,'freelancer/index.html',params)
        return redirect("homeFreelancer")
      if params['count']=="0":
          messages.error(request, "Invalid credentials! Please try again")
          return redirect("homeFreelancer")


def signOut(request):
  if 'mainName' not in request.session:
    params={'loginStatus':'no'}
    return render(request,'freelancer/index.html',params)
  else:
      del request.session['mainName']
      del request.session['mainPass']
      del request.session['mainId']
      del request.session['login']
      return redirect("homeFreelancer")


def myProfile(request):
  data= freelancer.objects.all()
  name = request.session.get('mainName')
  a=freelancer.objects.get(username=name)
  if request.method=='POST':
    fs = FileSystemStorage()
    change = freelancer.objects.get(id=a.id)
    try:
      if change.image == "/freelancer/images/dp.png":
        pass
      else:
        change.image.delete()
    except IntegrityError :
      messages.warning(request, "Opps Something goes wrong")
    change.category = request.POST['category']
    change.sub_category = request.POST['subcategory']
    change.image = request.FILES['image']
    change.save()
    a=freelancer.objects.get(username=name)
    params={'name':name,'id':a.id,'x':a}
    return render(request,'freelancer/profile.html',params)
  else:
    a=freelancer.objects.get(username=name)
    params={'name':name,'id':a.id,'x':a}
    return render(request,'freelancer/profile.html',params)

def updateProfile(request,edit_id):
    edit_id = int(edit_id)
    data2=freelancer.objects.filter(id=edit_id).first
    name = request.session.get('mainName')
    
    if request.method=="POST":
        change = freelancer.objects.get(id=edit_id)
        
        change.name = request.POST['name']
        change.username = request.POST['username']
        change.email = request.POST['email']
        change.password = request.POST['password']
        #change.image = request.FILES['image']
        try:
          change.save()
          messages.success(request, " Your details has been successfully updated")
          params = {"edit_id":edit_id,'x':data2,'name':name}
          return render(request,'freelancer/updateProfile.html',params)
        except IntegrityError as e:
          if 'UNIQUE constraint failed' in e.args[0]:
            messages.warning(request, "This name and email-id Exists already!. Please choose a unique name")
            return render(request,'freelancer/updateProfile.html',params)
    else:
      params = {"edit_id":edit_id,'x':data2,'name':name}
      return render(request,'freelancer/updateProfile.html',params)



def myGig(request):
  name = request.session.get('mainName')
  a=freelancer.objects.get(username=name)
  data=gig.objects.all()
  if request.method=='POST':
    title = request.POST['title']
    content=request.POST['desc']
    temp=gig(freelancerId=a.id,freelancer=a,title=title,content=content)
    temp.save()
    messages.success(request, " Your details has been successfully updated")
    params={'name':name,'x':a,'y':data}
    return render(request,'freelancer/gig.html',params)
    return render(request,'client/project.html',params)
  else:
    params={'name':name,'x':a,'y':data}
    return render(request,'freelancer/gig.html',params)

def editGig(request,edit):
  edit_id = int(edit)
  name = request.session.get('mainName')
  a=freelancer.objects.get(username=name)
  
  if request.method=='POST':
    change = gig.objects.get(gigId=edit_id)
    change.title = request.POST['title']
    change.content = request.POST['desc']
    change.save()
    data=gig.objects.all()
    messages.success(request, " Your content has been successfully updated")
    params={'name':name,'x':a,'y':data}
    return render(request,'freelancer/gig.html',params)
  else:
    data=gig.objects.get(gigId=edit_id)
    params={'name':name,'x':a,'y':data}
    return render(request,'freelancer/editGig.html',params)


def deleteGig(request,delete_id):
  name = request.session.get('mainName')
  a=freelancer.objects.get(username=name)
  data= gig.objects.all()
  delete_id = int(delete_id)
  params={'name':name,'x':a,'y':data,"delete_id":delete_id}
  delete = gig.objects.get(gigId=delete_id)
  delete.delete()
  messages.error(request, " successfully Deleted ")
  return render(request,'freelancer/gig.html',params)

lst = []




def testExam(request):




  a = test.objects.all()
  paginator = Paginator(a,1)
  try:
    page= int(request.GET.get('page','1'))
  except:
    page = 1
  try :
    questions= paginator.page(page)
  except(ExmtyPage,InvalidPage):
    questions= paginator.page(paginator.num.pages)

  name = request.session.get('mainName')
  change=freelancer.objects.get(username=name)
  if request.method=='POST':
    ans = request.POST['ans']
    if ans=="pass":
      change.rating = '1'
      change.save()
      request.session['mainReview'] = change.rating
      messages.success(request, "you have successfully pass the exam and got a review of 1 as a biginner ")
      return redirect('homeFreelancer')
    else :
      messages.error(request, " successfully post request  fail")
  else:
    params = {'data':a,"questions":questions}
    return render(request,'freelancer/test.html',params)



def save_ans(request):
  ans = request.GET['ans']
  lst.append(ans)

def result(request):

  answers = test.objects.all()
  anslist = []
  for i in answers:
    anslist.append(i.answer)
  #newly added
  name = request.session.get('mainName')
  change=freelancer.objects.get(username=name)
  score =0
  for i in range(len(lst)):
      if lst[i]==anslist[i]:
          score +=1

  anslist.clear()
  lst.clear()
  answers = test.objects.all()
  for i in answers:
    anslist.append(i.answer)

  if score >2:
    change.rating = '1'
    change.save()
    request.session['mainReview']='1'
    messages.success(request, "You have successfully clear the exam. Now you can create you'r GIG and bid on projects")
    params={'score':score,'lst':lst,'flag':'1'}
    return render(request,'freelancer/result.html',params)
  else:
    messages.info(request, "Sorry !! your have not clear the exam.")
    params={'score':score,'lst':lst,'flag':'0'}
    return render(request,'freelancer/result.html',params)

 

def displayRequests(request):
  a = requestByClient.objects.all()
  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  data= project.objects.all()
  params={"x":b,'y':a,'data':data}
  #x : freelancer and y : client 
  return render(request,'freelancer/displayRequests.html',params)


def acceptRequest(request):
  a = requestByClient.objects.all()
  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  data= project.objects.all()
  if request.method=='POST':
    freelancerName = request.POST['freelancer']
    projectId = request.POST['projectId']
    clientName = request.POST['client']
    k=client.objects.get(name=clientName)
    try :
      temp=chatlits(projectId=projectId,client=k,freelancer=b)
      temp.save()
      messages.success(request, " You have accepted the request check on the chat list")
      params={"x":b,'y':a,'data':data}
      return render(request,'freelancer/displayRequests.html',params)
    except IntegrityError as e:
      if 'UNIQUE constraint failed' in e.args[0]:
        messages.warning(request, "You have already accepted this request")
        params={"x":b,'y':a,'data':data}
        return render(request,'freelancer/displayRequests.html',params)
  else:
    params={"x":b,'y':a,'data':data}
    return render(request,'freelancer/displayRequests.html',params)


def chat(request):
  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  c= chatlits.objects.all()
  params = {'x':b,'chat':c}
  return render(request,'freelancer/chat.html',params)


def public(request):
  c= project.objects.all()
  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  d= chatlits.objects.all()
  params={'x':c,'client':d,'y':b}
  return render(request,'freelancer/public.html',params)

def qvProject(request, myid):

  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  projectList = project.objects.all()
  data = project.objects.get(projectId=myid);
  params={'project':data}
  if request.method=='POST':
    projectId = request.POST['id']
    clientId = request.POST['client']
    content = request.POST['desc']
    temp = requestByFreelancer( freelancer= b,clientId=clientId,projectId=projectId,content=content)
    try:
      temp.save()
      messages.success(request, " Request has been successfully sent ")
    except IntegrityError as e:
      if 'UNIQUE constraint failed' in e.args[0]:
        messages.warning(request, "The request has already been sent")
    return render(request,'freelancer/qvProject.html',params)
  else:
    return render(request,'freelancer/qvProject.html',params)


def MyTimeline(request):
  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  c= chatlits.objects.all()
  params = {'x':b,'chat':c}
  return render(request,'freelancer/timeline.html',params)

def viewTimeline(request,x):
  name = request.session.get('mainName')
  b=freelancer.objects.get(username=name)
  projectList = project.objects.all()
  chatdata = chatlits.objects.get(projectId=x,freelancer=b)
  data = project.objects.get(projectId=x);
  
  if request.method=='POST':
    text=request.POST.get('text')
    p =request.POST.get('projectNo')
    temp=timelineFC(text= text, freelancer=b,client= chatdata.client, flag=name, project=data)
    temp.save()
    k = timelineFC.objects.all()
    params={'project':data,'text':k,'freelancer':b}
    return render(request,'freelancer/viewTimeline.html',params)
  else:
    k = timelineFC.objects.all()
    params={'project':data,'text':k,'freelancer':b}
    return render(request,'freelancer/viewTimeline.html',params)

def staticChat(request):
  pass
    
  #return redirect(f"/blog/{post.slug}")

def uploadFiles(request,t):
  projectList= chatlits.objects.get(projectId=t)
  p= project.objects.get(projectId=t)
  if request.method=="POST":
    f = request.FILES['files']
    temp=trashFiles(project=p,freelancer=projectList.freelancer,client=projectList.client,flag=projectList.freelancer.username,data=f)
    temp.save()
    messages.success(request, " Successfully uploaded")
    files = trashFiles.objects.all()
    params={'project':projectList,'files':files}
    return render(request,'freelancer/uploadFiles.html',params)
  else:
    files = trashFiles.objects.all()
    params={'project':projectList,'files':files}
    return render(request,'freelancer/uploadFiles.html',params)


def makeReport(request,z):
  p= chatlits.objects.get(projectId=z)
  params={'project':p}
  if request.method=='POST':
    
    
    try:
      temp=report(freelancer=p.freelancer.username,client=p.client.username, flag=p.freelancer.username)
      temp.save()
      messages.success(request, "Successfully reported")
      return render(request,'freelancer/makeReport.html',params)

    except IntegrityError as e:
      if 'UNIQUE constraint failed' in e.args[0]:
        messages.warning(request, "Already reported")
        return render(request,'freelancer/makeReport.html',params)
    
    
  else:
    return render(request,'freelancer/makeReport.html',params)