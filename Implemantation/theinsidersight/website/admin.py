from django.contrib import admin
from website import models

admin.register(models.UserProfile)
admin.register(models.Post)
admin.register(models.reply_Post)
admin.register(models.Follower_List)
admin.register(models.Notification)