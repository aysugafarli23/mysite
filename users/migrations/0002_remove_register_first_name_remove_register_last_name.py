# Generated by Django 5.0.6 on 2024-07-09 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='register',
            name='last_name',
        ),
    ]