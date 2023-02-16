from django.contrib import admin
from .models import MusicBlog, Vote

# Register your models here.
admin.site.register(MusicBlog)
admin.site.register(Vote)