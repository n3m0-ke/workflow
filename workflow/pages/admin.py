from django.contrib import admin
from .models import Category, Tags, PhotoGallery, Image, Project, Task, TaskNotification, Instruction, ProposedTitleSubText, ArticleSection, Article, UserNotification

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskNotification)
admin.site.register(Instruction)
admin.site.register(ProposedTitleSubText)
admin.site.register(ArticleSection)
admin.site.register(Article)
admin.site.register(UserNotification)
admin.site.register(PhotoGallery)
admin.site.register(Image)
admin.site.register(Tags)
admin.site.register(Category)