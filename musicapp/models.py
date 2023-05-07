from django.db import models
from  django.contrib.auth.models import User

# Create your models here.

VOTE_CHOICES = (
    ('this is so good', 'THIS IS SO GOOD'),
    ('good but no replay value', 'GOOD BUT NO REPLAY VALUE'),
    ('i dont like this', 'I DONT LIKE THIS'),
)


class MusicBlog(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
 

class Vote(models.Model):
       vote = models.CharField(max_length=100, choices=VOTE_CHOICES,  blank=True, null=True)




