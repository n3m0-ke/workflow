# Generated by Django 4.2.1 on 2023-07-08 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_bioline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='laguages',
            new_name='languages',
        ),
    ]
