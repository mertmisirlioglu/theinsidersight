# Generated by Django 2.2.1 on 2020-01-12 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20200112_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='publist_time',
            new_name='publish_time',
        ),
    ]
