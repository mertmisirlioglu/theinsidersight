# Generated by Django 2.2.1 on 2020-02-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200127_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
