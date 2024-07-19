# Generated by Django 5.0.6 on 2024-07-19 20:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_title', models.CharField(max_length=255)),
                ('lesson_image', models.FileField(blank=True, null=True, upload_to='lesson_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_title', models.CharField(max_length=200)),
                ('module_image', models.FileField(blank=True, null=True, upload_to='module_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_title', models.CharField(max_length=200)),
                ('body', models.TextField(blank=True, null=True)),
                ('content_image', models.FileField(blank=True, null=True, upload_to='content_images/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='content_audio/')),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='recordings/')),
                ('video_link', models.URLField(blank=True, null=True)),
                ('content_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='module.module'),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('score_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='module.content')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=200)),
                ('section_lesson', models.ManyToManyField(to='module.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='content_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.section'),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('audio_file_alloy', models.FileField(blank=True, null=True, upload_to='words_audio/')),
                ('audio_file_nova', models.FileField(blank=True, null=True, upload_to='words_audio/')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='module.content')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='customer_recordings/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.word')),
            ],
        ),
    ]
