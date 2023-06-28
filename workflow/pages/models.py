from django.db import models
from users.models import Profile, Director, Editor, Journalist

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    start_date = models.DateField()
    end_date_time = models.DateTimeField()
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.title} Project'

class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True)
    journalists = models.ManyToManyField(Journalist, related_name='tasks')

    def __str__(self):
        return f'{self.title} Task'

class Article(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='article')
    article_text = models.TextField(null=True)

    def __str__(self):
        return f'{self.task.title} Task Article'

class PhotoGallery(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='photo_gallery')

    def __str__(self):
        return f'{self.task.title} Task Photo Gallery'

class Image(models.Model):
    photo_gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photo_gallery')

    def __str__(self):
        return f'{self.photo_gallery.task.title} Task Photo Gallery Image'

class Instruction(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, on_delete=models.SET_NULL, null=True)
    instruction = models.TextField()

    def __str__(self):
        return f'{self.task.title} Task\'s Instruction for {self.journalist.user.first_name} {self.journalist.user.last_name}'


