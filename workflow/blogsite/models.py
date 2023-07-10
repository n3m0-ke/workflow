from django.db import models

# Create your models here.
class UserContactMessage(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField()
    subject = models.CharField(max_length=40, null=True)
    message = models.TextField()
    message_time = models.DateTimeField()
