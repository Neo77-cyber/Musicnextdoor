from django.db import models
from  django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

VOTE_CHOICES = (
    ('i\m adding this to my playlist', 'I\'M ADDING THIS TO MY PLAYLIST'),
    ('good but no replay value', 'GOOD BUT NO REPLAY VALUE'),
    ('meh put it in a trash', 'MEH PUT THIS IN A TRASH'),
)

class MusicBlog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    total_votes = models.IntegerField(default=0)
    vote1_count = models.IntegerField(default=0)
    vote1_percent = models.FloatField(default=0)
    vote2_count = models.IntegerField(default=0)
    vote2_percent = models.FloatField(default=0)
    vote3_count = models.IntegerField(default=0)
    vote3_percent = models.FloatField(default=0)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    

    def __str__(self):
        return self.title if self.title else ''
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(MusicBlog, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.comment
 
class Vote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(MusicBlog, on_delete=models.CASCADE)
    vote = models.CharField(max_length=100, choices=VOTE_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_vote_counts()


    def update_vote_counts(self):
        post = self.post
        total_votes = Vote.objects.filter(post=post).count()
        vote1_count = Vote.objects.filter(post=post, vote='i\m adding this to my playlist').count()
        vote2_count = Vote.objects.filter(post=post, vote='good but no replay value').count()
        vote3_count = Vote.objects.filter(post=post, vote='meh put it in a trash').count()

        vote1_percent = round((vote1_count / total_votes) * 100, 2) if total_votes != 0 else 0
        vote2_percent = round((vote2_count / total_votes) * 100, 2) if total_votes != 0 else 0
        vote3_percent = round((vote3_count / total_votes) * 100, ) if total_votes != 0 else 0

        post.total_votes = total_votes
        post.vote1_count = vote1_count
        post.vote1_percent = vote1_percent
        post.vote2_count = vote2_count
        post.vote2_percent = vote2_percent
        post.vote3_count = vote3_count
        post.vote3_percent = vote3_percent
        post.save()

    def __str__(self) -> str:
        return self.vote







