from django.contrib import admin
from .models import Project, Task, TaskNotification, Instruction, ProposedTitleSubText

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskNotification)
admin.site.register(Instruction)
admin.site.register(ProposedTitleSubText)
