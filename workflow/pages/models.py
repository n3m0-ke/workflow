from django.db import models
from django.contrib.auth.models import User
from users.models import Profile, Director, Editor, Journalist
from django.utils import timezone

class ProjectStatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DEACTIVATED = 'deactivated', 'Deactivated'

class TaskStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ASSIGNED = 'assigned', 'Assigned'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    REJECTED = 'rejected', 'Rejected'
    APPROVED = 'approved', 'Approved'

class SubmissionStatusChoices(models.TextChoices):
    REJECTED = 'rejected', 'Rejected'
    IN_PROGRESS = 'in_progress', 'In Progress'
    SUBMITTED = 'submitted', 'Submitted'

class TaskNotificationTypes(models.TextChoices):
    INFO = 'info', 'Info'
    DANGER = 'danger', 'Danger'
    WARNING = 'warning', 'Warning'
    SUCCESS = 'success', 'Success'


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    date_of_creation = models.DateTimeField(null=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default=ProjectStatusChoices.ACTIVE, choices=ProjectStatusChoices.choices)
    
    def __str__(self):
        return f'{self.title} Project'

class Tags(models.Model):
    tag_name = models.CharField(max_length=20)

class Category(models.Model):
    category_name = models.CharField(max_length=20)

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()    
    start_date = models.DateField(null=True)
    deadline = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tags, related_name='tags')
    journalists = models.ManyToManyField(Journalist, related_name='tasks')  
    publication_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, default=TaskStatusChoices.PENDING, choices=TaskStatusChoices.choices)
    progress = models.IntegerField(default=10)
    submission_status = models.CharField(max_length=20, default=SubmissionStatusChoices.IN_PROGRESS, choices=SubmissionStatusChoices.choices)

    def __str__(self):
        return f'{self.title} Task'
    
    @property
    def remaining_days(self):
        remaining_time = self.deadline - timezone.now()
        remainig_days = remaining_time.days

        return remainig_days
    
    @property
    def average_rating(self):
        if self.reviews.all():
            sum = 0
            counter = 0
            for review in self.review.all():
                rating = review.rating
                sum += rating
                counter += 1
            
            average_rating = round(sum/counter)
        else:
            average_rating = 0

        return average_rating
            

class Reviews(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=70)
    review = models.TextField()
    rating = models.IntegerField()
    review_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.task.title} Review'
    



class Article(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='article')
    title = models.CharField(max_length=30, null=True)
    subtext = models.CharField(max_length=70, null=True)
    article_text = models.TextField(null=True)

    def __str__(self):
        return f'{self.task.title} Task Article'

class ProposedTitleSubText(models.Model):
    title = models.CharField(max_length=30)
    subtext = models.CharField(max_length=70)
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null='true')

class ArticleSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_sections')
    section_title = models.CharField(max_length=40, null=True)
    section_text = models.TextField(null=True)
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE, related_name='journalist', unique=False)
    submission_status = models.CharField(max_length=20, default=SubmissionStatusChoices.IN_PROGRESS, choices=SubmissionStatusChoices.choices)



class PhotoGallery(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photo_gallery', null=True)    
    title = models.CharField(max_length=20, null=True)
    subtext = models.CharField(max_length=30, null=True)
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE, related_name='photo_journalist', null=True, unique=False)
    submission_status = models.CharField(max_length=20, default=SubmissionStatusChoices.IN_PROGRESS, choices=SubmissionStatusChoices.choices)

    def __str__(self):
        return f'{self.article.title} Task Photo Gallery'


class Image(models.Model):
    photo_gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='photo_gallery', null=True)
    name = models.CharField(max_length=5, default='one')

    def __str__(self):
        return f'{self.photo_gallery.article.title} Task Photo Gallery Image'

class Instruction(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, on_delete=models.SET_NULL, null=True)
    instruction = models.TextField()
    type = models.CharField(max_length=10, default='original')

    def __str__(self):
        return f'{self.task.title} Task\'s Instruction for {self.journalist.user.first_name} {self.journalist.user.last_name}'
    
class TaskNotification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    current_status = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20, default=TaskNotificationTypes.INFO, choices=TaskNotificationTypes.choices) 
    creation_time = models.DateTimeField(null=True)

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class SectionRejections(models.Model):
    article_section = models.ForeignKey(ArticleSection, on_delete=models.CASCADE, related_name="section_rejections")
    reason = models.TextField()

class GalleryRejections(models.Model):
    photo_gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE, related_name="gallery_rejections")
    reason = models.TextField()

class TaskRejections(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_rejections")
    reason = models.TextField()
