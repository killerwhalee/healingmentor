from django.db import models


class Post(models.Model):
    user = models.ForeignKey("common.User", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=16)

    title = models.CharField(max_length=32)
    body = models.TextField()
    
    def __str__(self) -> str:
        return self.title
