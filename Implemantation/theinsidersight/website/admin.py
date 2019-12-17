from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(reply_Post)
admin.site.register(Follower_List)
admin.site.register(Notification)
