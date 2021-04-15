from django.db import models
from datetime import datetime
from django.utils.timezone import now
class client(models.Model):
    cid = models.AutoField(primary_key=True)
    username=models.CharField(max_length=20,default="")
    name = models.CharField(max_length=40,default="")
    email = models.CharField(max_length=40,default="")
    password = models.CharField(max_length=30,default="")
    date = models.DateField()
    image = models.ImageField(upload_to="client/images",default="")
    class Meta:
        unique_together = ["username", "name", "email"]
    def __str__(self):
        return self.name
class project(models.Model):
    projectId = models.AutoField(primary_key=True)
    clientId=models.IntegerField()
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    category=models.CharField(max_length=30,default="")
    subcategory=models.CharField(max_length=30,default="")
    budget = models.IntegerField(default=0)
    date_start = models.DateField()
    deanline = models.DateField()
    content=models.TextField()
    publishCategory=models.CharField(max_length=30,default="")
    def __str__(self):
        return self.title +"by "+ self.client.name

class requestByClient(models.Model):
    requestId=models.AutoField(primary_key=True)
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    freelancerId=models.IntegerField(default=0)
    projectId=models.IntegerField(default=0)
    class Meta:
        unique_together = ["client", "projectId"]
    def __str__(self):
        return self.client.name

