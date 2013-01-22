from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.db.utils import DatabaseError


class UserProfile(User):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    jabber = models.CharField(max_length=255, null=True)
    skype = models.CharField(max_length=255, null=True)
    other_contacts = models.TextField(null=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)


class Request(models.Model):
    class Meta:
        ordering = ['-priority', '-created_at']

    created_at = models.DateTimeField(auto_now=True)
    path = models.TextField()
    method = models.CharField(max_length=10)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s' % (self.path, self.method)


class ModelLog(models.Model):
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    created_at = models.DateTimeField(auto_now=True)
    app_label = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)

    @classmethod
    def log(cls, instance, action):
        # exclude ModelLog changes from log
        if not isinstance(instance, ModelLog):
            try:
                entry = ModelLog(
                    app_label=instance._meta.app_label,
                    model_name=instance.__class__.__name__,
                    action=action
                )
                entry.save()
            except DatabaseError:
                pass


def log_update_create(sender, instance, created, **kwargs):
        ModelLog.log(instance, ModelLog.ACTION_CREATE if created else ModelLog.ACTION_UPDATE)


def log_delete(sender, instance, **kwargs):
    ModelLog.log(instance, ModelLog.ACTION_DELETE)

post_save.connect(log_update_create, dispatch_uid='log_update_create')
post_delete.connect(log_delete, dispatch_uid='log_delete')
