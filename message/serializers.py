from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "subject",
            "content",
            "created_at",
            "is_read",
        ]
        read_only_fields = ["sender", "is_read"]
