# Generated by Django 2.2.1 on 2020-01-26 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(choices=[('Post', 'Post'), ('Soru', 'Soru'), ('Yorum', 'Yorum')], max_length=20)),
                ('category', models.CharField(choices=[('Aşk', 'Aşk'), ('Dost Kazığı', 'Dost Kazığı'), ('Avcılar', 'Avcılar'), ('Civcivler', 'Civcivler'), ('Profesyonellik içerenler', 'Profesyonellik içerenler'), ('Diğer', 'Diğer')], max_length=50)),
                ('publish_date', models.DateField()),
                ('publish_time', models.TimeField(auto_now_add=True)),
                ('content', models.TextField(max_length=2000)),
                ('replycount', models.IntegerField(default=0)),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('E', 'Erkek'), ('K', 'Kadın')], max_length=1)),
                ('faculty', models.CharField(choices=[('Mühendislik', 'Mühendislik'), ('Mimarlık', 'Mimarlık'), ('Fen-Edebiyat', 'Fen-Edebiyat'), ('İktisadi-İdari', 'İktisadi-İdari'), ('Güzel Sanatlar', 'Güzel Sanatlar')], max_length=20)),
                ('birthdate', models.DateField()),
                ('createdat', models.DateField()),
                ('postCount', models.IntegerField(blank=True, null=True)),
                ('point', models.IntegerField(default=0)),
                ('following', models.ManyToManyField(through='website.Follower_List', to='website.UserProfile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='reply_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_post_type', models.CharField(choices=[('Soru', 'Soru'), ('Yorum', 'Yorum')], max_length=20)),
                ('main_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_post_main_post', to='website.Post')),
                ('replied_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_post_replied_post', to='website.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='publish_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.UserProfile'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('isReaded', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='follower_list',
            name='followedby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_list_followed_by', to='website.UserProfile'),
        ),
        migrations.AddField(
            model_name='follower_list',
            name='followingto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_list_following_to', to='website.UserProfile'),
        ),
    ]