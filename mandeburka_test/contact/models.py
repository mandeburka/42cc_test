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


class Request(models.Model):
    created_at = models.DateTimeField()
    path = models.TextField()
    method = models.CharField(max_length=10)
