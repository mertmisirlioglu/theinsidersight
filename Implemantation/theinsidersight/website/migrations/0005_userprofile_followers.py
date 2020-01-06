# Generated by Django 2.2.1 on 2020-01-06 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20200106_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(through='website.Follower_List', to='website.UserProfile'),
        ),
    ]