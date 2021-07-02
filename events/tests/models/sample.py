from django.db import models


class Sample(models.Model):
    name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'my_app'
