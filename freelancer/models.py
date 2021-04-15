from django.db import models
from datetime import datetime
from client.models import project
from client.models import client
from django.utils.timezone import now
class freelancer(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=20,default="")
    name = models.CharField(max_length=40,default="")
    email = models.CharField(max_length=40,default="")
    password = models.CharField(max_length=30,default="")
    rating= models.IntegerField(default=0)
    levels = models.CharField(max_length=20,default="")
    category = models.CharField(max_length=40,default="")
    sub_category = models.CharField(max_length=40, default="")
    date = models.DateField()
    image = models.ImageField(upload_to="freelancer/images",default="")
    class Meta:
        unique_together = ["username", "name", "email"]
    def __str__(self):
        return self.name
class gig(models.Model):
    gigId = models.AutoField(primary_key=True)
    freelancerId=models.IntegerField(default=0)
    freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField()
    def __str__(self):
        return self.title

class test(models.Model):
    qid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=40,default="")
    question = models.CharField(max_length=500,default="")
    q1 = models.CharField(max_length=500,default="")
    q2 = models.CharField(max_length=500,default="")
    q3 = models.CharField(max_length=500,default="")
    q4 = models.CharField(max_length=500,default="")
    answer = models.CharField(max_length=500,default="")
    def __str__(self):
        return self.question


class requestByFreelancer(models.Model):
    requestId=models.AutoField(primary_key=True)
    freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
    clientId=models.IntegerField(default=0)
    projectId=models.IntegerField(default=0)
    content=models.TextField(default=" ")
    class Meta:
        unique_together = ["freelancer", "projectId"]
    def __str__(self):
        return self.freelancer.name


class timelineFC(models.Model):
    sno= models.AutoField(primary_key=True)
    text=models.TextField()
    freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    project=models.ForeignKey(project, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    flag=models.CharField(max_length=50)
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.text[0:20] + "..." + "by" + " (" + self.freelancer.username + " & "+ self.client.username+" )"

class trashFiles(models.Model):
    sno= models.AutoField(primary_key=True)
    project=models.ForeignKey(project, on_delete=models.CASCADE)
    freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    data = models.FileField(upload_to="freelancer/files",default="")
    flag=models.CharField(max_length=50)
    def __str__(self):
        return self.freelancer.username

class report(models.Model):
    sno=models.AutoField(primary_key=True)
    freelancer =models.CharField(max_length=40)
    client = models.CharField(max_length=40)
    flag = models.CharField(max_length=40)
    class Meta:
        unique_together = ["freelancer", "client"]
    def __str__(self):
        return self.flag