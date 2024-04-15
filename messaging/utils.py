from .models import Messaging
from django.db import models


def get_message(message_id=None, user=None):
    """
    Fetches a message from the database based on the provided ID and user.
    Args:
        message_id (int, optional): The ID of the message to retrieve.
        user (User, optional): The user for whom to fetch the message.
    Returns:
        Messaging or QuerySet: The message object if found, or queryset of messages if user is provided but not message_id, otherwise None.
    """
    try:
        if message_id and user:
            return Messaging.objects.get(models.Q(id=message_id, sender=user) | models.Q(id=message_id, receiver=user))
        elif user:
            return Messaging.objects.filter(models.Q(sender=user) | models.Q(receiver=user))
        else:
            return None
    except Messaging.DoesNotExist:
        return None
