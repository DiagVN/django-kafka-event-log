from django.db import models


class Events(models.Model):
    topic = models.CharField(max_length=200, null=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
