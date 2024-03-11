from django.db import models
from django.contrib.auth.models import User

from _config.settings.base import MEDIA_ROOT
from _config.utils import uuid_filepath


class MultiplyerData(models.Model):
    """
    Multiplyer Data

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


class QuestionData(models.Model):
    pass


class GuidedMeditationData(models.Model):
    """
    Guided Meditation Data

    Data table for Respiratory Graph

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        "date created", auto_now=False, auto_now_add=True
    )
    score = models.IntegerField("recorded points", default=0)
    note = models.TextField("user note")


class RespiratoryGraphData(models.Model):
    """
    Respiratory Graph Data

    Data table for Respiratory Graph

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        "date created", auto_now=False, auto_now_add=True
    )
    csv_data = models.FileField(
        "csv data file", upload_to=uuid_filepath, max_length=None, null=False
    )
    score = models.IntegerField("recorded points", default=0)
    note = models.TextField("user note")

    # Override delete() to delete connected csv file
    def delete(self, *args, **kargs):
        import os

        if self.csv_data:
            os.remove(os.path.join(MEDIA_ROOT, self.csv_data.path))

        super().delete(*args, **kargs)


class SustainedAttentionData(models.Model):
    """
    Sustained Attention Data

    Data table for Respiratory Data

    """

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        "date created", auto_now=False, auto_now_add=True
    )
    csv_data = models.FileField(
        "csv data file", upload_to=uuid_filepath, max_length=None
    )
    rate_data = models.JSONField("rading data", null=True)
    score = models.IntegerField("recorded points", default=0)
    note = models.TextField("user notes")

    # Override delete() to delete connected csv file
    def delete(self, *args, **kargs):
        import os

        if self.csv_data:
            os.remove(os.path.join(MEDIA_ROOT, self.csv_data.path))

        super().delete(*args, **kargs)
