import pdb
from django.shortcuts import render, redirect
from .models import MusicBlog, Vote, Comment
from .forms import VoteForm, CreatePostForm, CreateCommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator


# Create your views here.

def home(request):
    posts = MusicBlog.objects.all().order_by('-date')

    createpost_form = CreatePostForm()
    if request.method == 'POST' and request.user.is_authenticated:
        createpost_form = CreatePostForm(request.POST, request.FILES)
        if createpost_form.is_valid():
            new_post = createpost_form.save(commit=False)
            new_post.author = request.user       
            new_post.save()
            createpost_form = CreatePostForm() 

    paginator = Paginator(posts, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    return render(request, 'home.html', {'page_obj': page_obj, 'createpostform': createpost_form})






def single_post(request, pk):
    post = get_object_or_404(MusicBlog, id=pk)
    comment_form = CreateCommentForm()
    vote_form = VoteForm()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():  
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            comment_form = CreateCommentForm()   
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
                vote = vote_form.save(commit=False)
                vote.author = request.user
                vote.post = post
                vote.save()
                vote_form = VoteForm()
                post.vote1_count = Vote.objects.filter(post=post, vote='i\m adding this to my playlist').count()
                post.vote2_count = Vote.objects.filter(post=post, vote='good but no replay value').count()
                post.vote3_count = Vote.objects.filter(post=post, vote='meh put it in a trash').count()
                post.total_votes = post.vote1_count + post.vote2_count + post.vote3_count

                if post.total_votes > 0:
                    post.vote1_percent = (post.vote1_count / post.total_votes) * 100
                    post.vote2_percent = (post.vote2_count / post.total_votes) * 100
                    post.vote3_percent = (post.vote3_count / post.total_votes) * 100
                else:
                    post.vote1_percent = 0
                    post.vote2_percent = 0
                    post.vote3_percent = 0

                post.save()

    users_comments = Comment.objects.filter(post=post)

    vote_instance = post

    context = {
        'post': post,
        'comment_form': comment_form,
        'users_comments': users_comments,
        'vote_instance': vote_instance,
        'vote_form': vote_form,
    }

    return render(request, 'single_post.html', context)














def votecount(request):
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
    
    return render(request, 'votecount.html', context)

def signin(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            else:
                messages.info(request, 'Invalid username or password.. Please try again.')
                return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render (request,'signin.html')

def register(request):
    form_name = UserForm()
    if request.method =="POST":
        form_name = UserForm(request.POST)
        if form_name.is_valid():
            form_name.save()
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Password not secure') 
            return redirect('register')
    else:
        context = {'form_name':form_name}
        
    return render(request, 'register.html', context )
         
