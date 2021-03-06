import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from notifications.models import Notification
from notifications.signals import notify
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from website.forms import PostForm, ReplyPostForm
from website.models import UserProfile, Post, reply_Post, Follower_List
from website.tokens import account_activation_token


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
    user_profile = UserProfile.objects.get(user=request.user)
    post_list = Post.objects.none()
    for user in user_profile.following.all():
        post_list = post_list | Post.objects.all().filter(post_type='Post', publish_by=user).all()
    # print(getNotifications(request))

    post_list = create_paginator(request, post_list)
    return render(request, 'anasayfa.html', {'post_list': post_list})


def getNotifications(request):
    if request.user.is_anonymous:
        return {}

    n = Notification.objects.all().filter(recipient=request.user)

    return {
        'notification_list': n,
        'count': n.count(),
    }


@my_login_required
def confessions_view(request):
    confession_list = Post.objects.all().filter(post_type='Post').order_by('-pk')
    confession_list = create_paginator(request, confession_list)
    return render(request, 'itiraflar.html', {'confession_list': confession_list})


@my_login_required
def ask_confessions_view(request):
    return render(request, 'prof.html', {'confession_list': category_post_getter(request, 'Aşk')})


@my_login_required
def dost_confessions_view(request):
    return render(request, 'prof.html', {'confession_list': category_post_getter(request, 'Dost Kazığı')})


@my_login_required
def civciv_confessions_view(request):
    return render(request, 'prof.html', {'confession_list': category_post_getter(request, 'Civcivler')})


@my_login_required
def avci_confessions_view(request):
    return render(request, 'prof.html', {'confession_list': category_post_getter(request, 'Avcılar')})


@my_login_required
def prof_confessions_view(request):
    return render(request, 'prof.html', {'confession_list': category_post_getter(request, 'Profesyonellik içerenler')})


@my_login_required
def diger_confessions_view(request):
    return render(request, 'prof.html', {'confession_list': category_post_getter(request, 'Diğer')})


def category_post_getter(request, category):
    confession_list = Post.objects.all().filter(category=category)
    confession_list = create_paginator(request, confession_list)
    return confession_list


@my_login_required
def leader_board_view(request):
    point_list = UserProfile.objects.all().order_by("-point")
    user_profile = UserProfile.objects.get(user=request.user)
    index_list = (*point_list,)
    index = index_list.index(user_profile) + 1
    page = request.GET.get('page', 1)
    paginator = Paginator(point_list, 5)
    try:
        point_list = paginator.page(page)
    except PageNotAnInteger:
        point_list = paginator.page(1)
    except EmptyPage:
        point_list = paginator.page(paginator.num_pages)

    context = {'index': index,
               'user_info': user_profile,
               'point_list': point_list
               }
    return render(request, 'siralama.html', context)


@my_login_required
def discover_view(request):
    user_profile = UserProfile.objects.all().get(user=request.user)
    user_likes = Post.objects.all().filter(likes=request.user)
    if user_likes.count() > 0:
        ask = 0
        dost = 0
        avcılar = 0
        civciv = 0
        prof = 0
        diger = 0

        for post in user_likes:

            if post.category == 'Aşk':
                ask += 1
            elif post.category == 'Dost Kazığı':
                dost += 1
            elif post.category == 'Avcılar':
                avcılar += 1
            elif post.category == 'Civcivler':
                civciv += 1
            elif post.category == 'Profesyonellik içerenler':
                prof += 1
            elif post.category == 'Diğer':
                diger += 1
        category = {"Aşk": ask, "Dost Kazığı": dost, "Avcılar": avcılar, "Civcivler": civciv,
                    "Profesyonellik içerenler": prof, "Diğer": diger}

        category = sorted(category, key=category.get)


        post_list = Post.objects.all().filter(category=category[len(category) - 1]).exclude(
            publish_by=user_profile).order_by('-pk')
        post_list = post_list | Post.objects.all().filter(category=category[len(category) - 2]).exclude(
            publish_by=user_profile).order_by('-pk')
        post_list = post_list | Post.objects.all().filter(category=category[len(category) - 3]).exclude(
            publish_by=user_profile).order_by('-pk')
    else:
        post_list = Post.objects.all().order_by('-pk')

    post_list = create_paginator(request, post_list)
    return render(request, 'kesfet.html', {'post_list': post_list})


@my_login_required
def user_search_view(request):
    if request.method == "POST":
        search_input = request.POST['search-input']
        results = UserProfile.objects.filter(user__username__icontains=search_input)
        empty = False
        if len(results) == 0:
            empty = True
        return render(request,'kullaniciara.html',{'user_list':results,'empty':empty})
    else:
        return render(request,'kullaniciara.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.email_confirmed:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Hesabınız onaylanmamış.Lütfen mailinizdeki linke tıklayarak onaylayınız.')
                return redirect('login')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
            return redirect('login')
    else:
        return render(request, 'login.html')




def register_view(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        birthdate = request.POST['date']
        createdat = datetime.datetime.now()
        faculty = request.POST['Bölüm']
        gender = request.POST['gender']
        converted = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        if str(email).split('@')[1] != 'isik.edu.tr':
            messages.error(request,'Güvenliğiniz için sadece Işık mailiniz ile kayıt olabilirsiniz.')
            return redirect('register')
        if password1 != password2:
            messages.error(request, 'İki şifre eşleşmiyor.')
            return redirect('register')
        if len(password1) < 8:
            messages.error(request, 'Şifre 8 karakterden küçük olamaz.')
            return redirect('register')
        if converted.year > createdat.year:
            messages.error(request, 'Geçersiz doğum tarihi.Geçerli bir tarih giriniz.')
            return redirect('register')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            messages.error(request, 'Email sistemde kayıtlı.Lütfen başka bir email giriniz.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Kullanıcı adı sistemde kayıtlı.Lütfen başka bir kullanıcı adı giriniz.')
            return redirect('register')

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password1)
        profile = UserProfile(gender=gender, faculty=faculty, user=user, birthdate=birthdate, createdat=createdat)
        # user_test = UserProfile.objects.get(pk=13)
        profile.save()
        subject = 'Aramıza hoşgeldin - The Insider Sight'
        current_site = get_current_site(request)
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

        messages.success(request, 'Onay maili belirttiğiniz maile gönderildi.')
        return redirect('register')
    else:
        return render(request, 'register.html')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user_profile = UserProfile.objects.get(user=user)
            user_profile.email_confirmed = True
            user_profile.save()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, ('Onaylama linki yanlış veya kullanılmış.'))
            return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('login')


@my_login_required
def my_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    followers_count = Follower_List.objects.all().filter(followingto=user_profile).count()
    post_list = Post.objects.all().filter(publish_by=user_profile).order_by('-pk')
    post_count = post_list.count()
    post_list = create_paginator(request, post_list)
    context = {'user_profile': user_profile,
               'post_list': post_list,
               'post_count': post_count,
               'followers_count': followers_count}
    return render(request, 'profile.html', context)


@my_login_required
def send_post(request):
    form = PostForm(request.POST or None)
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        post_content = request.POST.get('post-content', 'hey')
        if (len(post_content) > 255):
            messages.error(request, 'Post 255 karekteri geçemez.')
            return render(request, 'post.html', {'user_profile': user_profile})
        post_type = 'Post'
        category = request.POST.get('category')
        publish_date = datetime.datetime.now()
        publish_by = UserProfile.objects.get(user=request.user)
        likecount = 0
        replycount = 0
        post = Post(post_type=post_type, category=category, publish_date=publish_date, publish_by=publish_by,
                    content=post_content, replycount=replycount)
        post.save()
        return redirect('home')
    else:
        return render(request, 'post.html', {'user_profile': user_profile})


@my_login_required
def reply_post(request, post_id):
    main_post = get_object_or_404(Post, pk=post_id)
    isReply = reply_Post.objects.all().filter(replied_post=main_post)
    user_profile = UserProfile.objects.get(user=request.user)
    if isReply.count() > 0:
        for reply in isReply:
            main_post = reply.main_post

    reply_list = reply_Post.objects.all().filter(main_post=main_post)
    form = ReplyPostForm(request.POST or None)
    context = {'main_post': main_post, 'reply_list': reply_list, 'form': form, 'user_profile': user_profile}
    if request.method == "POST":
        post_content = request.POST.get('post-content', 'hey')
        if (len(post_content) > 255):
            messages.error(request, 'Post 255 karekteri geçemez.')
            return render(request, 'reply_post.html', context)
        post_type = 'Yorum'
        category = 'Diğer'
        publish_date = datetime.datetime.now()
        publish_by = UserProfile.objects.get(user=request.user)
        likecount = 0
        replycount = 0
        post = Post(post_type=post_type, category=category, publish_date=publish_date, publish_by=publish_by,
                    content=post_content, replycount=replycount)
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
        target_url = main_post.get_reply_url()
        notify.send(request.user, recipient=main_post.publish_by.user, verb='postuna yorum yaptı.',
                    description=target_url)
        return redirect('home')
    else:
        return render(request, 'reply_post.html', context)


@my_login_required
def question_page(request):
    post_list = Post.objects.all().filter(post_type='Soru').order_by('-pk')
    post_list = create_paginator(request, post_list)
    return render(request, 'sorular.html', {'post_list': post_list})


@my_login_required
def answer_page(request):
    answer_list = reply_Post.objects.all().filter(reply_post_type='Soru').order_by('-pk')
    answer_list = create_paginator(request, answer_list)
    return render(request, 'cevaplar.html', {'answer_list': answer_list})


def create_paginator(request, list):
    page = request.GET.get('page', 1)
    paginator = Paginator(list, 20)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


@my_login_required
def notifications_mobile_view(request):
    context = getNotifications(request)
    context['notification_list'] = create_paginator(request,context['notification_list'])
    return render(request, 'mobile-notification.html',context)


@my_login_required
def send_question(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        post_content = request.POST.get('post-content', 'hey')
        if(len(post_content)>255):
            messages.error(request, 'Post 255 karekteri geçemez.')
            return render(request, 'post.html', {'user_profile': user_profile})
        post_type = 'Soru'
        category = request.POST.get('category')
        publish_date = datetime.datetime.now()
        publish_by = UserProfile.objects.get(user=request.user)
        likecount = 0
        replycount = 0
        post = Post(post_type=post_type, category=category, publish_date=publish_date, publish_by=publish_by,
                    content=post_content, replycount=replycount)
        post.save()
        return redirect('home')
    else:
        return render(request, 'post.html', {'user_profile': user_profile})


class post_like_api_toggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id=None, format=None):
        obj = get_object_or_404(Post, pk=post_id)
        updated = False
        liked = False

        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
                if obj.publish_by != user_profile:
                    obj.publish_by.point -= 10
            else:
                liked = True
                obj.likes.add(user)
                target_url = obj.get_reply_url()
                notify.send(user, recipient=obj.publish_by.user, verb='postunu beğendi.', description=target_url)
                if obj.publish_by != user_profile:
                    obj.publish_by.point += 10
            updated = True
        obj.publish_by.save()
        data = {
            'updated': updated,
            'liked': liked
        }
        return Response(data)


@my_login_required
def profile_view(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    own_user = get_object_or_404(UserProfile, user=request.user)
    followers_count = Follower_List.objects.all().filter(followingto=user).count()
    post_list = Post.objects.all().filter(publish_by=user).order_by('-pk')
    post_count = post_list.count()
    post_list = create_paginator(request, post_list)
    context = {'user_profile': user,
               'own_user': own_user,
               'post_list': post_list,
               'post_count': post_count,
               'followers_count': followers_count}
    return render(request, "kullanıcı profil sayfası.html", context)

@staff_member_required
def delete_post(request, post_id):
    deleted_post = Post.objects.get(pk=post_id)
    deleted_post.delete()
    return redirect('confessions')


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
                target_url = user_profile.get_profile_url()
                notify.send(user, recipient=obj.user, verb='seni takip etti.', description=target_url)

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
def admin_user(request):
    user_list = UserProfile.objects.all()
    context = {'user_list': user_list
               }

    return render(request, 'admin/takipçiler admin.html', context)

@staff_member_required
def delete_user(request, user_id):
    user = UserProfile.objects.all().get(pk=user_id)
    user.user.delete()
    user.delete()
    return redirect('adminkullanicilar')

@my_login_required
def user_followers(request):
    user_profile = UserProfile.objects.all().get(user=request.user)
    follower_list = Follower_List.objects.all().filter(followingto=user_profile)
    return render(request, 'followers.html', {'follower_list': follower_list})

@my_login_required
def user_following(request):
    following_list = UserProfile.objects.all().get(user=request.user).following.all()
    return render(request, 'following.html', {'following_list': following_list})
