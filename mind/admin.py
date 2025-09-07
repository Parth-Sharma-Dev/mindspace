from django.contrib import admin
from .models import Room, Message, ForumPost, ForumComment

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(ForumPost)
admin.site.register(ForumComment)