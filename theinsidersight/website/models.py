from django.contrib.auth.models import User
from django.db import models


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
    following = models.ManyToManyField('self', symmetrical=False, through='Follower_List')
    postCount = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_profile_url(self):
        return f"/profil/{self.pk}/"

    def get_follow_api_url(self):
        return f"/takip/api/{self.pk}/"

    def __str__(self):
        return self.user.username

    def get_delete_user_url(self):
        return f"/sil/{self.pk}/"


class Post(models.Model):
    Post_Type = (
        ('Post', 'Post'),
        ('Soru', 'Soru'),
        ('Yorum', 'Yorum')
    )

    Category = (
        ('Aşk', 'Aşk'),
        ('Dost Kazığı', 'Dost Kazığı'),
        ('Avcılar', 'Avcılar'),
        ('Civcivler', 'Civcivler'),
        ('Profesyonellik içerenler', 'Profesyonellik içerenler'),
        ('Diğer', 'Diğer')
    )
    publish_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=Post_Type)
    category = models.CharField(max_length=50, choices=Category)
    publish_date = models.DateField()
    publish_time = models.TimeField(auto_now_add=True)
    content = models.TextField(max_length=2000)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    replycount = models.IntegerField(default=0)

    def get_reply_url(self):
        return f"/cevapla/{self.pk}/"

    def get_like_api_url(self):
        return f"/begen/api/{self.pk}/"

    def get_delete_post_url(self):
        return f"/post/sil/{self.pk}/"


class reply_Post(models.Model):
    Reply_Post_Type = (
        ('Soru', 'Soru'),
        ('Yorum', 'Yorum')
    )
    reply_post_type = models.CharField(max_length=20, choices=Reply_Post_Type)
    main_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='%(class)s_main_post')
    replied_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='%(class)s_replied_post')


class Follower_List(models.Model):
    followedby = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='%(class)s_followed_by')
    followingto = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='%(class)s_following_to')


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    isReaded = models.BooleanField(default=False)
