from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Specialties(models.Model):
    specialty = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.specialty}'

class LanguageChoices(models.Model):
    language = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.language}'

class CapacityChoices(models.TextChoices):
    WRITER = 'writer', 'Writer Journalist'
    PHOTOJOURNALIST = 'photojournalist', 'Photo Journalist'
    EDITOR = 'editor', 'Editor'
    DIRECTOR = 'director', 'Director'

class Employee(models.Model):
    first_name = models.CharField(max_length=20)
    other_names = models.CharField(max_length=30)
    email = models.EmailField()
    id_card_number = models.CharField(max_length=10, unique=True)
    capacity = models.CharField(max_length=20, choices=CapacityChoices.choices)
    specialties = models.ManyToManyField(Specialties, related_name='specialties', null=True)
    languages = models.ManyToManyField(LanguageChoices, related_name='languages', null=True)
    date_of_employment = models.DateField(null=True)

    def __str__(self):
        return f'{self.capacity} {self.first_name} {self.other_names} Record'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.png', upload_to='profile_pictures')
    email = models.EmailField()
    id_card_number = models.CharField(max_length=10)
    capacity = models.CharField(max_length=20, choices=CapacityChoices.choices)
    bioline = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Journalist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CapacityChoices.choices)

    def __str__(self):
        return f'{self.user.first_name} Journalist Record'

class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} Editor Record'

class Director(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} Director Record'

