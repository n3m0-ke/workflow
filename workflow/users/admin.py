from django.contrib import admin
from .models import Profile, Employee, LanguageChoices, Specialties

# Register your models here.
admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(LanguageChoices)
admin.site.register(Specialties)

