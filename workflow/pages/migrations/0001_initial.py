# Generated by Django 4.2.1 on 2023-07-08 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('subtext', models.CharField(max_length=70, null=True)),
                ('article_text', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=40, null=True)),
                ('section_text', models.TextField(null=True)),
                ('submission_status', models.CharField(choices=[('rejected', 'Rejected'), ('in_progress', 'In Progress'), ('submitted', 'Submitted')], default='in_progress', max_length=20)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_sections', to='pages.article')),
                ('journalist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journalist', to='users.journalist')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('date_of_creation', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('deactivated', 'Deactivated')], default='active', max_length=20)),
                ('director', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.director')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('start_date', models.DateField(null=True)),
                ('deadline', models.DateTimeField(null=True)),
                ('end_date_time', models.DateTimeField(null=True)),
                ('publication_date', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('rejected', 'Rejected'), ('approved', 'Approved')], default='pending', max_length=20)),
                ('progress', models.IntegerField(default=10)),
                ('submission_status', models.CharField(choices=[('rejected', 'Rejected'), ('in_progress', 'In Progress'), ('submitted', 'Submitted')], default='in_progress', max_length=20)),
                ('categories', models.ManyToManyField(related_name='categories', to='pages.category')),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.editor')),
                ('journalists', models.ManyToManyField(related_name='tasks', to='users.journalist')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.project')),
                ('tags', models.ManyToManyField(related_name='tags', to='pages.tags')),
            ],
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskRejections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_rejections', to='pages.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('current_status', models.CharField(max_length=20, null=True)),
                ('type', models.CharField(choices=[('info', 'Info'), ('danger', 'Danger'), ('warning', 'Warning'), ('success', 'Success')], default='info', max_length=20)),
                ('creation_time', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.task')),
            ],
        ),
        migrations.CreateModel(
            name='SectionRejections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('article_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_rejections', to='pages.articlesection')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
                ('review_date', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='pages.task')),
            ],
        ),
        migrations.CreateModel(
            name='ProposedTitleSubText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('subtext', models.CharField(max_length=70)),
                ('article', models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='pages.article')),
                ('journalist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.journalist')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, null=True)),
                ('subtext', models.CharField(max_length=30, null=True)),
                ('submission_status', models.CharField(choices=[('rejected', 'Rejected'), ('in_progress', 'In Progress'), ('submitted', 'Submitted')], default='in_progress', max_length=20)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_gallery', to='pages.article')),
                ('journalist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_journalist', to='users.journalist')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', models.TextField()),
                ('type', models.CharField(default='original', max_length=10)),
                ('journalist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.journalist')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.task')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='photo_gallery')),
                ('name', models.CharField(default='one', max_length=5)),
                ('photo_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pages.photogallery')),
            ],
        ),
        migrations.CreateModel(
            name='GalleryRejections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('photo_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_rejections', to='pages.photogallery')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='pages.task'),
        ),
    ]
