# Generated by Django 4.2.1 on 2023-05-22 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('body', models.TextField(blank=True, max_length=5000, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_votes', models.IntegerField(default=0)),
                ('vote1_count', models.IntegerField(default=0)),
                ('vote1_percent', models.FloatField(default=0)),
                ('vote2_count', models.IntegerField(default=0)),
                ('vote2_percent', models.FloatField(default=0)),
                ('vote3_count', models.IntegerField(default=0)),
                ('vote3_percent', models.FloatField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.CharField(blank=True, choices=[('this is so good', 'THIS IS SO GOOD'), ('good but no replay value', 'GOOD BUT NO REPLAY VALUE'), ('i dont like this', 'I DONT LIKE THIS')], max_length=100, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicapp.musicblog')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicapp.musicblog')),
            ],
        ),
    ]
