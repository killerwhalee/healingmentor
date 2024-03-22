from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from _config.utils import uuid_filepath


"""
Extended User Profile Model

This model provided additional information of user.
Isolated from login information, it seems more secured.
"""


# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        "User Profile Image",
        upload_to=uuid_filepath,
        default="/static/images/profile-default.png",
    )
    
    fullname = models.CharField("Fullname of user", max_length=16)
    classname = models.CharField("Current class", blank=True, max_length=1)
    
    def __str__(self) -> str:
        return f"Profile ({self.user})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, fullname=instance.username)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
