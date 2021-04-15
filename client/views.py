from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from math import ceil
import datetime
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import client, project,requestByClient
from freelancer.models import freelancer,gig, requestByFreelancer, timelineFC, trashFiles , report
from chat.models import chatlits
from django.db import models
from django.core.files.storage import FileSystemStorage

def homeClient(request):
    loginStatus = request.session.get('clientLogin')
    if loginStatus == 'yes':
        name = request.session.get('clientName')
        params={'name':name}
        return render(request,'client/index.html',params)
    else:
        return render(request,'client/index.html')



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
          temp = client(username=username,name=name,email=email,password=pass1,date=datetime.datetime.now(),image="/freelancer/images/dp.png")
          temp.save()
          messages.success(request, " Your account has been successfully created")
          return redirect('homeClient')
        except IntegrityError as e:
          if 'UNIQUE constraint failed' in e.args[0]:
            messages.warning(request, "This name and email-id Exists already!. Please choose a unique name")
            return redirect('homeClient')

    else:
        messages.warning(request, "404 - Not found | Something goes wrong ")
        return redirect('homeClient')



def authentication(request,credential):
  data= client.objects.all()
  count = 0
  for i in data:
    if ((i.username == credential["username"]) and (i.password == credential["password"])):
      count = 1
      a=client.objects.get(username=credential["username"])
      params={'name':credential["username"],'id':a.cid,"count":"1"}
      request.session['clientName']= credential["username"]
      request.session['clientPass']= credential["password"]
      request.session['clientId'] = a.cid
      request.session['clientLogin'] = 'yes'
      return params
      break
  if count==0:
    params={"count":"0"}
    return params


def signIn(request):
    data= client.objects.all()
    if request.method=='POST':
      username = request.POST['loginusername']
      password = request.POST['loginpassword']
      credential={"username":username,"password":password}
      params = authentication(request,credential)
      if params['count']=="1":
        messages.success(request, "Successfully Logged In")
        #return render(request,'client/index.html',params)
        return redirect("homeClient")
      if params['count']=="0":
          messages.error(request, "Invalid credentials! Please try again")
          return redirect("homeClient")


def signOut(request):
  if 'clientName' not in request.session:
    params={'loginStatus':'no'}
    return render(request,'client/index.html',params)
  else:
      del request.session['clientName']
      del request.session['clientPass']
      del request.session['clientId']
      del request.session['clientLogin']
      return redirect("homeClient")

def myProfile(request):
  data= client.objects.all()
  name = request.session.get('clientName')
  a=client.objects.get(username=name)

  if request.method=='POST':
    fs = FileSystemStorage()
    change = client.objects.get(cid=a.cid)
    try:
      if a.image == "/freelancer/images/dp.png":
        pass
      else:
        a.image.delete()
    except IntegrityError :
      messages.warning(request, "Opps Something goes wrong")
    a.image = request.FILES['image']
    a.save()
    a=client.objects.get(username=name)
    params={'name':name,'id':a.cid,'x':a}
    return render(request,'client/profile.html',params)
  else:  
    params={'name':name,'id':a.cid,'x':a}
    return render(request,'client/profile.html',params)


def myProject(request):
  name = request.session.get('clientName')
  data= project.objects.all()
  a=client.objects.get(username=name)
  if request.method=='POST':
    title = request.POST['title']
    category = request.POST['category']
    subcategory = request.POST['subcategory']
    budget= request.POST['price']
    content=request.POST['desc']
    deadline=request.POST['deadline']
    select=request.POST['select']
    temp=project(clientId=a.cid,client=a,title=title,category=category,subcategory=subcategory,budget=budget,date_start=datetime.datetime.now(),deanline=deadline,content=content,publishCategory=select)
    temp.save()
    params={'name':name,'x':a,'data':data}
    return render(request,'client/project.html',params)
  else:
    params={'name':name,'x':a,'data':data}
    return render(request,'client/project.html',params)

def deleteProject(request,delete_id):
  name = request.session.get('clientName')
  data= project.objects.all()
  a=client.objects.get(username=name)
  delete_id = int(delete_id)
  params={'name':name,'x':a,'data':data,"delete_id":delete_id}
  delete = project.objects.get(projectId=delete_id)
  try:
    data= chatlits.objects.get(projectId=delete_id)
    data.delete()
  except IntegrityError as e:
    pass
  delete.delete()
  messages.error(request, " successfully Deleted ")
  return render(request,'client/project.html',params)




def updateProject(request,update_id):
  name = request.session.get('clientName')
  data= project.objects.all()
  a=client.objects.get(username=name)
  if request.method=="POST":
    change = project.objects.get(projectId=update_id)
    change.title = request.POST['title']
    change.category = request.POST['category']
    change.subcategory = request.POST['subcategory']
    change.budget= request.POST['price']
    change.content=request.POST['desc']
    change.deadline=request.POST['deadline']
    change.publishCategory=request.POST['select']
    change.save()
    messages.success(request, "Changes are successfully made")
    params={'name':name,'x':a,'data':data}
    return render(request,'client/project.html',params)
  else:
    params={'name':name,'x':a,'data':data,'id':update_id}
    return render(request,'client/editProject.html',params)

def public(request):
  mem_send = 'not_post'
  if request.method=='POST':

    select=request.POST['select']
    if (select == 'all'):
      mem_send = 'not_post'
      post_select ='null'
    else:
      post_select = select
      mem_send = 'post'

  if mem_send =='post':
    name = request.session.get('clientName')
    a=client.objects.get(username=name)
    all_data=[]
    cat_freelancer=freelancer.objects.values('category', 'id')
    cats= {item["category"] for item in cat_freelancer}
    for cat in cats:
      temp=freelancer.objects.filter(category=cat,levels=post_select)
      n = len(temp)
      nSlides = n // 4 + ceil((n / 4) - (n // 4))
      all_data.append([temp, range(1, nSlides), nSlides])
    params={'all_data':all_data ,'username':name,'cli_id':a,'email':a.email,'mem_send':mem_send,'post_select':post_select}

    return render(request,'client/public.html',params)
  else:
    data= freelancer.objects.all()
    length = len(data)
    all_data=[]
    cat_freelancer=freelancer.objects.values('category', 'id')
    cats= {item["category"] for item in cat_freelancer}
    for cat in cats:
        temp=freelancer.objects.filter(category=cat)
        n = len(temp)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        all_data.append([temp, range(1, nSlides), nSlides])
    params={'all_data':all_data,'mem_send':'not_post'}
    return render(request,'client/public.html',params)

def qvFreelancer(request, myid):
  flag = 0
  category_validation_flag = 0
  data=freelancer.objects.get(id=myid)
  projectList = project.objects.all()
  name = request.session.get('clientName')
  a=client.objects.get(username=name)
  dataGig=gig.objects.all()
  if request.method== 'POST':
    projectId = request.POST['projectId']
    for i in projectList:
      if (str(i.projectId) == projectId):
        objects_of_id = project.objects.get(projectId=projectId)
        flag = 1
        if(data.levels == objects_of_id.publishCategory):
          category_validation_flag = 1  
        else:
          category_validation_flag = 0  
        break
    if ( (flag == 1) and (category_validation_flag ==1)):
      flag = 0
      category_validation_flag = 0 
      temp = requestByClient(client=a, freelancerId=myid,projectId=projectId)
      try:
        temp.save()
        messages.success(request, " successfully linked ")
        params={'data':data,'myid':myid,'name':name,'x':data,'y':dataGig}
        return render(request, "client/qvFreelancer.html",params)
      except IntegrityError as e:
        if 'UNIQUE constraint failed' in e.args[0]:
          messages.warning(request, "The request has already been sent")
          params={'data':data,'myid':myid,'name':name,'x':data,'y':dataGig}
          return render(request, "client/qvFreelancer.html",params)
    elif ((flag == 1) and (category_validation_flag ==0)):
      flag = 0
      category_validation_flag = 0 
      messages.error(request, " Can't linked project. Because of invalid category linkage. The freelancer is  "+ data.levels +" and your project category is "+ objects_of_id.publishCategory)
      params={'data':data,'myid':myid,'name':name,'x':data,'y':dataGig}
      return render(request, "client/qvFreelancer.html",params)
    else:
      messages.error(request, " Can't linked porject doesn't exist with this id "+projectId)
      params={'data':data,'myid':myid,'name':name,'x':data,'y':dataGig}
      return render(request, "client/qvFreelancer.html",params)
  else:
    params={'data':data,'myid':myid,'name':name,'x':data,'y':dataGig}
    return render(request, "client/qvFreelancer.html",params)


def updateProfile(request,edit_id):

  edit_id = int(edit_id)
  data2=client.objects.filter(cid=edit_id).first
  name = request.session.get('clientName')
  
  if request.method=="POST":
      change = client.objects.get(cid=edit_id)
      
      change.name = request.POST['name']
      change.username = request.POST['username']
      change.email = request.POST['email']
      change.password = request.POST['password']
      #change.image = request.FILES['image']
      try:
        change.save()
        messages.success(request, " Your details has been successfully updated")
        params = {"edit_id":edit_id,'x':data2,'name':name}
        return render(request,"client/updateProfile.html",params)
      except IntegrityError as e:
        if 'UNIQUE constraint failed' in e.args[0]:
          messages.warning(request, "This name and email-id Exists already!. Please choose a unique name")
          return render(request,"client/updateProfile.html",params)
  else:
    params = {"edit_id":edit_id,'x':data2,'name':name}
    return render(request,"client/updateProfile.html",params)


def chat(request):
  name = request.session.get('clientName')
  b=client.objects.get(username=name)
  c= chatlits.objects.all()
  params = {'x':b,'chat':c}
  return render(request,'client/chat.html',params)



def displayRequests(request):
  a = requestByFreelancer.objects.all()
  name = request.session.get('clientName')
  b=client.objects.get(username=name)
  data= project.objects.all()
  params={"client":b,'freelancer':a,'data':data}
  if request.method=="POST":
    freelancerName = request.POST['freelancer']
    projectId = request.POST['projectId']
    clientName = request.POST['client']
    k=freelancer.objects.get(username=freelancerName)
    try :
      temp=chatlits(projectId=projectId,client=b,freelancer=k)
      temp.save()
      messages.success(request, " You have accepted the request check on the chat list")
      return render(request,'client/displayRequests.html',params)
    except IntegrityError as e:
      if 'UNIQUE constraint failed' in e.args[0]:
        messages.warning(request, "You have already accepted this request")
        return render(request,'client/displayRequests.html',params)
  else:  
    return render(request,'client/displayRequests.html',params)



def acceptRequest(request):
  a = requestByFreelancer.objects.all()
  name = request.session.get('clientName')
  b=client.objects.get(username=name)
  data= project.objects.all()
  params={"client":b,'freelancer':a,'data':data}
  print("working")
  return render(request,'client/displayRequests.html',params)



def MyTimeline(request):
   name = request.session.get('clientName')
   b=client.objects.get(username=name)
   c= chatlits.objects.all()
   params = {'x':b,'chat':c}
   return render(request,'client/timeline.html',params)

def viewTimeline(request,x):
  name = request.session.get('clientName')
  data= project.objects.get(projectId=x)
  a=client.objects.get(username=name)
  chatdata = chatlits.objects.get(projectId=x,client=a)
  if request.method=='POST':
    text=request.POST.get('text')
    p =request.POST.get('projectNo')
    temp=timelineFC(text= text, freelancer=chatdata.freelancer, client=a, flag=name,project=data)
    temp.save()
    k = timelineFC.objects.all()
    params={'project':data,'text':k,'freelancer':chatdata.freelancer}
    return render(request,'client/viewTimeline.html',params)
  else:
    k = timelineFC.objects.all()
    params={'project':data,'text':k,'freelancer':chatdata.freelancer}
    return render(request,'client/viewTimeline.html',params)

def uploadFiles(request,t):
  projectList= chatlits.objects.get(projectId=t)
  p= project.objects.get(projectId=t)
  if request.method=="POST":
    f = request.FILES['files']
    temp=trashFiles(project=p,freelancer=projectList.freelancer,client=projectList.client,flag=projectList.client.username,data=f)
    temp.save()
    messages.success(request, " Successfully uploaded")
    files = trashFiles.objects.all()
    params={'project':projectList,'files':files}
    return render(request,'client/uploadFiles.html',params)
  else:
    files = trashFiles.objects.all()
    params={'project':projectList,'files':files}
    return render(request,'client/uploadFiles.html',params)

def payment(request,u):
  p= project.objects.get(projectId=u)
  params={'project':p,'project':p}
  return render(request,'client/payment.html',params)
def giveReviews(request,v):
  p= chatlits.objects.get(projectId=v)
  r = report.objects.all()
  params={'project':p,'report':r}
  if request.method=='POST':
    rev = request.POST['reviews']
    
    if rev == 'good':
      no = 5
    elif rev =='verygood':
      no = 10
    change = freelancer.objects.get(username=p.freelancer.username)
    change.rating += no
    change.save()
    messages.success(request, " Thankyou for your review")
    return render(request,'client/giveReviews.html',params)
  else:
    return render(request,'client/giveReviews.html',params)


def makeReport(request,z):
  p= chatlits.objects.get(projectId=z)
  params={'project':p}
  if request.method=='POST':
    
    
    try:
      temp=report(freelancer=p.freelancer.username,client=p.client.username, flag=p.client.username)
      temp.save()
      messages.success(request, "Successfully reported")
      return render(request,'client/payment.html',params)

    except IntegrityError as e:
      if 'UNIQUE constraint failed' in e.args[0]:
        messages.warning(request, "Already reported")
        return render(request,'client/payment.html',params)
    
    
  else:
    return render(request,'client/payment.html',params)