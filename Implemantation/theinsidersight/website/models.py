from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    GENDER = (
        ('E', 'Erkek'),
        ('K', 'Kadın'),
    )
    FACULTY = (
        ('Mühendislik', 'Mühendislik'),
        ('Mimarlık', 'Mimarlık'),
        ('Fen-Edebiyat', 'Fen-Edebiyat'),
        ('İktisadi-İdari', 'İktisadi-İdari'),
        ('Güzel Sanatlar', 'Güzel Sanatlar')
    )

    gender = models.CharField(max_length=1, choices=GENDER)
    faculty = models.CharField(max_length=20, choices=FACULTY)
    birthdate = models.DateField()
    createdat = models.DateField()
    postCount = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)




class Post(models.Model):
    Post_Type = (
        ('Post', 'Post'),
        ('Soru', 'Soru'),
    )

    Category = (
        ('Aşk', 'Aşk'),
        ('Dost Kazığı', 'Dost Kazığı'),
        ('Avcılar', 'Avcılar'),
        ('Civcivler', 'Civcivler'),
        ('Profesyonellik içerenler', 'Profesyonellik içerenler'),
        ('Diğer', 'Diğer')
    )
    publish_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=Post_Type)
    category = models.CharField(max_length=20, choices=Category)
    publish_date = models.DateField()
    content = models.TextField(max_length=2000)
    likecount = models.IntegerField(default=0)
    replycount = models.IntegerField(default=0)


class reply_Post(Post):
    main_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='%(class)s_main_post')
    replied_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='%(class)s_replied_post')


class Follower_List(models.Model):
    followedby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_followed_by')
    followingto = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_following_to')


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    isReaded = models.BooleanField(default=False)
