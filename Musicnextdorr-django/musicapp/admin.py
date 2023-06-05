from django.contrib import admin
from .models import MusicBlog, Vote, Comment

# Register your models here.
admin.site.register(MusicBlog)
admin.site.register(Vote)
admin.site.register(Comment)
