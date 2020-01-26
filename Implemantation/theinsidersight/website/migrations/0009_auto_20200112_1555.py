# Generated by Django 2.2.1 on 2020-01-12 15:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20200112_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publist_time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateField(),
        ),
    ]