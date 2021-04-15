from django.contrib.auth import get_user_model
from django.db import models
from client.models import client
from freelancer.models import freelancer
User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)



class chatlits(models.Model):
    projectId=models.IntegerField(default=0, primary_key=True)
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
    class Meta:
        unique_together = ["freelancer", "projectId","client"]
    def __str__(self):
        return self.client.name +" - "+ self.freelancer.name