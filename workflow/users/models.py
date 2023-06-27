from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class CapacityChoices(models.TextChoices):
    WRITER = 'writer', 'Writer Journalist'
    PHOTOJOURNALIST = 'photojournalist', 'Photo Journalist'
    EDITOR = 'editor', 'Editor'
    DIRECTOR = 'director', 'Director'

class Employee(models.Model):
    first_name = models.CharField(max_length=20)
    other_names = models.CharField(max_length=30)
    email = models.EmailField()
    id_card_number = models.CharField(max_length=10)
    capacity = models.CharField(max_length=20, choices=CapacityChoices.choices)

    def __str__(self):
        return f'{self.first_name} {self.other_names} Employee Record'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    email = models.EmailField()
    id_card_number = models.CharField(max_length=10)
    capacity = models.CharField(max_length=20, choices=CapacityChoices.choices)

    def __str__(self):
        return f'{self.user.username} Profile'

