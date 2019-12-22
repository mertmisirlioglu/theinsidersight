
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from website.forms import ExtendedUserCreationForm, ProfileForm, PostForm
    # , ReplyPostForm
from website.models import UserProfile, Post, reply_Post
import datetime


def home_view(request):
    post_list = Post.objects.all()
    content = {'post_list' :post_list}
    return render(request, 'anasayfa.html' ,content)


def confessions_view(request):
    confession_list = Post.objects.all().filter(post_type='Post')
    content = {'confession_list' :confession_list}
    return render(request, 'itiraflar.html' ,content)


def answers_view(request):
    return render(request, 'cevaplar.html')


def leader_board_view(request):
    return render(request, 'siralama.html')


def discover_view(request):
    return render(request, 'kesfet.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    return render(request, 'register.html')


def signup(request):
    form = ExtendedUserCreationForm(request.POST or None)
    profile = ProfileForm(request.POST or None)
    if form.is_valid() and profile.is_valid():
        user = form.save()
        profile = profile.save(commit=False)
        profile.user = user
        profile.createdat = datetime.datetime.now()
        profile.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'register.html',
                      {'form': ExtendedUserCreationForm, 'profile_form': ProfileForm})


def my_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    age = datetime.datetime.now().year - user_profile.birthdate.year
    context = {'user': user, 'profile': user_profile, 'age': age}
    return render(request, 'profile.html', context)


def send_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.post_type = 'Post'
        post.publish_date = datetime.datetime.now()
        post.publish_by = request.user
        post.likecount = 0
        post.replycount = 0
        post.save()
        return redirect('home')
    else:
        return render(request ,'post.html' ,{'form' :form})


def reply_post(request ,post_id):
    main_post = get_object_or_404(Post, pk=post_id)
    reply_list = reply_Post.objects.all().filter(main_post=main_post)
    form = PostForm(request.POST or None)
    context = {'main_post':main_post, 'reply_list': reply_list, 'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.post_type = 'Post'
        post.publish_date = datetime.datetime.now()
        post.publish_by = request.user
        post.likecount = 0
        post.replycount = 0
        main_post.replycount += 1
        main_post.save()
        post.save()
        new_reply = reply_Post()
        new_reply.main_post = main_post
        new_reply.replied_post = post
        new_reply.save()
        return redirect('home')
    else:
        return render(request, 'reply_post.html' ,context)
