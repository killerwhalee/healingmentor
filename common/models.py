from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from core.utils import uuid_filepath


class UserManager(BaseUserManager):
    """
    Custom User Manager

    User authentication is made by access token.

    Therefore password of normal user is `None`.

    """

    use_in_migrations = True

    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)

        # Set admin permissions
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model

    This user model is designed for simplificatio.

    """

    objects = UserManager()

    # Username is used as primary key
    username = models.CharField(max_length=16, primary_key=True)

    # Basic permissions overwritten
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"


class Profile(models.Model):
    """
    Extended User Profile Model

    This model provided additional information of user.

    """

    user = models.OneToOneField("common.User", on_delete=models.CASCADE)
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
