from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(User):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    jabber = models.CharField(max_length=255, null=True)
    skype = models.CharField(max_length=255, null=True)
    other_contacts = models.TextField(null=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)


class Request(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    path = models.TextField()
    method = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s %s' % (self.path, self.method)


class ModelLog(models.Model):
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    created_at = models.DateTimeField(auto_now=True)
    app_lable = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
