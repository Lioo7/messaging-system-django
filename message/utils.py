from django.db import models

from .models import Message


def get_message(message_id=None, user=None):
    """
    Fetches a message from the database based on the provided ID and user.
    Args:
        message_id (int, optional): The ID of the message to retrieve.
        user (User, optional): The user for whom to fetch the message.
    Returns:
        Message or QuerySet: The message object if found, or queryset of messages if user is provided but not message_id, otherwise None.
    """
    try:
        if message_id and user:
            return Message.objects.get(models.Q(id=message_id, sender=user) | models.Q(id=message_id, receiver=user))
        elif user:
            return Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user))
        else:
            return None
    except Message.DoesNotExist:
        return None
