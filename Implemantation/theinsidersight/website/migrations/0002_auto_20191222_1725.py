# Generated by Django 2.2.1 on 2019-12-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='post',
            name='likecount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='replycount',
            field=models.IntegerField(default=0),
        ),
    ]
