from rest_framework import serializers
from .models import Room, Message, ForumPost, ForumComment
from .utils.pseudonyms import pseudonym_for

class MessageSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "text", "created_at", "display_name"]

    def get_display_name(self, obj):
        return pseudonym_for(obj.user_id, str(obj.room_id))

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "title", "description"]

class ForumCommentSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = ForumComment
        fields = ["id", "text", "created_at", "display_name", "replies"]

    def get_display_name(self, obj):
        return pseudonym_for(obj.user_id, str(obj.post_id))

    def get_replies(self, obj):
        return ForumCommentSerializer(obj.replies.all(), many=True).data

class ForumPostSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    comments = ForumCommentSerializer(many=True, read_only=True)

    class Meta:
        model = ForumPost
        fields = ["id", "title", "content", "created_at", "display_name", "comments"]

    def get_display_name(self, obj):
        return pseudonym_for(obj.user_id, str(obj.id))
