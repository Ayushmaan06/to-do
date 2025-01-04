from django.db import models
from django.contrib.auth.models import User

class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        unique_together = ('user', 'title')  # Enforces unique task titles per user

    def __str__(self):
        return self.title
