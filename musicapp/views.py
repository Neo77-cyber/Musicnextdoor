from django.shortcuts import render, redirect
from .models import MusicBlog, Vote
from .forms import BlogForm

# Create your views here.

def home(request):
    posts = MusicBlog.objects.all().order_by('-date')
    
    return render(request, 'home.html', {'posts': posts})

def post(request, pk):
    post = MusicBlog.objects.get(id = pk)

    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
    if form.is_valid():
            form.save()
            return redirect('votes')                 
    return render (request, 'post.html', {'post': post, 'form': form})


def votes(request):
    total_votes = Vote.objects.count() 
    vote1_count = Vote.objects.filter(vote='this is so good').count()
    vote1_percent = (vote1_count / total_votes) * 100  
    vote2_count = Vote.objects.filter(vote='good but no replay value').count()
    vote2_percent = (vote2_count / total_votes) * 100  
    vote3_count = Vote.objects.filter(vote='i dont like this').count()
    vote3_percent = (vote3_count / total_votes) * 100
  
    context = {
        'total_votes': total_votes,
        'vote1_count': vote1_count,
        'vote1_percent': vote1_percent,
        'vote2_count': vote2_count,
        'vote2_percent': vote2_percent,
        'vote3_count': vote3_count,
        'vote3_percent': vote3_percent,
    }
    
    return render(request, 'votes.html', context)

         
