from django.db import models
from django.conf import settings
import uuid

# ------------------ Rooms ------------------

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

# ------------------ Forum ------------------

class ForumPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    content = models.TextField()
    pseudonym = models.CharField(max_length=50)
    anon_id = models.CharField(max_length=64, db_index=True)  # <- new field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class ForumComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="comments")
    pseudonym = models.CharField(max_length=50)
    anon_id = models.CharField(max_length=64, db_index=True)  # <- new field
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
