# Generated by Django 4.2.1 on 2023-07-08 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Specialties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='default.png', upload_to='profile_pictures')),
                ('email', models.EmailField(max_length=254)),
                ('id_card_number', models.CharField(max_length=10)),
                ('capacity', models.CharField(choices=[('writer', 'Writer Journalist'), ('photojournalist', 'Photo Journalist'), ('editor', 'Editor'), ('director', 'Director')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Journalist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('writer', 'Writer Journalist'), ('photojournalist', 'Photo Journalist'), ('editor', 'Editor'), ('director', 'Director')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('other_names', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('id_card_number', models.CharField(max_length=10, unique=True)),
                ('capacity', models.CharField(choices=[('writer', 'Writer Journalist'), ('photojournalist', 'Photo Journalist'), ('editor', 'Editor'), ('director', 'Director')], max_length=20)),
                ('date_of_employment', models.DateField(null=True)),
                ('laguages', models.ManyToManyField(null=True, related_name='languages', to='users.languagechoices')),
                ('specialties', models.ManyToManyField(null=True, related_name='specialties', to='users.specialties')),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
