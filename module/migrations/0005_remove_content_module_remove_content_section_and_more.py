# Generated by Django 5.0.6 on 2024-06-20 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0004_rename_modules_section_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='module',
        ),
        migrations.RemoveField(
            model_name='content',
            name='section',
        ),
        migrations.AddField(
            model_name='section',
            name='contents',
            field=models.ManyToManyField(related_name='sections', to='module.content'),
        ),
    ]