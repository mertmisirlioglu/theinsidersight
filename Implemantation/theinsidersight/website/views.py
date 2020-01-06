from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.template import RequestContext
from infinite_scroll_pagination import serializers, paginator
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from website.forms import ExtendedUserCreationForm, ProfileForm, PostForm, ReplyPostForm
# , ReplyPostForm
from website.models import UserProfile, Post, reply_Post, Follower_List
from django.views.generic import RedirectView
import datetime
from django.contrib.auth.models import User


def my_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        else:
            return function(request, *args, **kw)

    return wrapper





@my_login_required
def home_view(request):
    post_list = Post.objects.all().filter(post_type='Post')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 20)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'anasayfa.html', {'post_list': posts})





@my_login_required
def confessions_view(request):
    confession_list = Post.objects.all().filter(post_type='Post')
    content = {'confession_list': confession_list}
    return render(request, 'itiraflar.html', content)


@my_login_required
def answers_view(request):
    return render(request, 'cevaplar.html')


@my_login_required
def leader_board_view(request):
    return render(request, 'siralama.html')


@my_login_required
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


@my_login_required
def my_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    age = datetime.datetime.now().year - user_profile.birthdate.year
    context = {'user': user, 'profile': user_profile, 'age': age}
    return render(request, 'profile.html', context)


@my_login_required
def send_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.post_type = 'Post'
        post.publish_date = datetime.datetime.now()
        post.publish_by = UserProfile.objects.get(user=request.user)
        post.likecount = 0
        post.replycount = 0
        post.save()
        return redirect('home')
    else:
        return render(request, 'post.html', {'form': form})


@my_login_required
def reply_post(request, post_id):
    main_post = get_object_or_404(Post, pk=post_id)
    reply_list = reply_Post.objects.all().filter(main_post=main_post)
    form = ReplyPostForm(request.POST or None)
    context = {'main_post': main_post, 'reply_list': reply_list, 'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.post_type = 'Yorum'
        post.category = 'Diğer'
        post.publish_date = datetime.datetime.now()
        post.publish_by = UserProfile.objects.get(user=request.user)
        post.likecount = 0
        post.replycount = 0
        main_post.replycount += 1
        main_post.save()
        post.save()
        new_reply = reply_Post()
        new_reply.main_post = main_post
        new_reply.replied_post = post
        if main_post.post_type == 'Soru':
            new_reply.reply_post_type = 'Soru'
        else:
            new_reply.reply_post_type = 'Yorum'
        new_reply.save()
        return redirect('home')
    else:
        return render(request, 'reply_post.html', context)


@my_login_required
def question_page(request):
    post_list = Post.objects.all().filter(post_type='Soru')
    content = {'post_list': post_list}
    return render(request, 'sorular.html', content)


@my_login_required
def answer_page(request):
    answer_list = reply_Post.objects.all().filter(reply_post_type='Soru')
    content = {'answer_list': answer_list}
    return render(request, 'cevaplar.html', content)


@my_login_required
def send_question(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.post_type = 'Soru'
        post.publish_date = datetime.datetime.now()
        post.publish_by = UserProfile.objects.get(user=request.user)
        post.likecount = 0
        post.replycount = 0
        post.save()
        return redirect('home')
    else:
        return render(request, 'post-question.html', {'form': form})


class post_like_api_toggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id=None, format=None):
        obj = get_object_or_404(Post, pk=post_id)
        updated = False
        liked = False

        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True

        data = {
            'updated': updated,
            'liked': liked
        }
        return Response(data)


def profile_view(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    own_user = get_object_or_404(UserProfile, user=request.user)
    context = {'user_profile': user,
               'own_user': own_user}
    return render(request, "kullanıcı profil sayfası.html", context)


class follow_api_toggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None, format=None):
        obj = get_object_or_404(UserProfile, pk=user_id)
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        if user.is_authenticated:
            updated = False
            followed = False

            if obj not in user_profile.following.all():
                followed = True
                user_profile.following.add(obj)
            else:
                followed = False
                user_profile.following.remove(obj)
            updated = True

        data = {
            'updated': updated,
            'followed': followed
        }
        return Response(data)


@staff_member_required
def cevaplaradmin_view(request):
    return render(request, 'admin/cevaplar-admin.html')

@staff_member_required
def itiraflaradmin_view(request):
    return render(request, 'admin/itiraflar-admin.html')

@staff_member_required
def kullanicilaradmin_view(request):
    return render(request, 'admin/kullanicilar-admin.html')