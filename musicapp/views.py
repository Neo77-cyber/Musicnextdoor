from django.shortcuts import render, redirect
from .models import MusicBlog, Vote
from .forms import BlogForm

# Create your views here.

def home(request):
    return render(request, 'home.html')


def blog(request):
    news = MusicBlog.objects.all()
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
    if form.is_valid():
            form.save()
            return redirect('vote') 
    

    return render(request, 'blog.html', {'news': news, 'form': form})

def vote(request):
    total_votes = Vote.objects.count()
    vote1 = Vote.objects.filter(vote = 'this is so good').count() 
    votepercent1 = vote1 / total_votes * (100)
    vote2 = Vote.objects.filter(vote = 'good but no replay value').count() 
    votepercent2 = vote2 / total_votes * (100)
    vote3 = Vote.objects.filter(vote = 'i dont like this').count() 
    votepercent3 = vote3 / total_votes * (100)

    context = {'total_votes': total_votes, 'vote1':vote1, 'votepercent1': votepercent1,
                'vote2':vote2, 'votepercent2': votepercent2, 'vote3':vote3, 
                'votepercent3': votepercent3}

   
    return render (request, 'vote.html', context )
