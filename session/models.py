from django.db import models
from django.contrib.auth.models import User

from _config.settings.base import MEDIA_ROOT
from _config.utils import uuid_filepath


class Multiplyer(models.Model):
    """
    Multiplyer

    Manages user tokens for score multiplying bonus time.

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE)

    # Daily Multiplyer
    daily_datetime = models.DateTimeField(
        "Last daily multiplyer creation", auto_now=False, auto_now_add=True
    )
    daily_tokens = models.IntegerField("Daily multiplyer left in seconds", default=900)

    # Hourly Multiplyer
    hourly_datetime = models.DateTimeField(
        "Last hourly multiplyer creation", auto_now=False, auto_now_add=True
    )
    hourly_tokens = models.IntegerField(
        "Hourly multiplyer left in seconds", default=300
    )


class Question(models.Model):
    """
    Questions

    Applied for all session (maybe)

    """

    question_1 = models.TextField(blank=True)
    question_2 = models.TextField(blank=True)
    question_3 = models.TextField(blank=True)
    question_4 = models.TextField(blank=True)


class GuidedMeditation(models.Model):
    """
    Guided Meditation

    Table for Guided Meditation

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        "date created", auto_now=False, auto_now_add=True
    )
    score = models.IntegerField("recorded points", default=0)
    lecture = models.CharField("lecture", max_length=50)
    question = models.ForeignKey("session.Question", on_delete=models.CASCADE)


class RespiratoryGraph(models.Model):
    """
    Respiratory Graph

    Table for Respiratory Graph

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        "date created", auto_now=False, auto_now_add=True
    )
    csv_data = models.FileField(
        "csv  file", upload_to=uuid_filepath, max_length=None, null=False
    )
    score = models.IntegerField("recorded points", default=0)
    question = models.ForeignKey("session.Question", on_delete=models.CASCADE)

    # Override delete() to delete connected csv file
    def delete(self, *args, **kargs):
        import os

        if self.csv_data:
            os.remove(os.path.join(MEDIA_ROOT, self.csv_data.path))

        super().delete(*args, **kargs)


class SustainedAttention(models.Model):
    """
    Sustained Attention

    Table for Sustained Attention

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        "date created", auto_now=False, auto_now_add=True
    )
    csv_data = models.FileField("csv  file", upload_to=uuid_filepath, max_length=None)
    rate_data = models.JSONField("rading ", null=True)
    score = models.IntegerField("recorded points", default=0)
    question = models.ForeignKey("session.Question", on_delete=models.CASCADE)

    # Override delete() to delete connected csv file
    def delete(self, *args, **kargs):
        import os

        if self.csv_data:
            os.remove(os.path.join(MEDIA_ROOT, self.csv_data.path))

        super().delete(*args, **kargs)
