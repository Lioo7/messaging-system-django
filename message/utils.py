from django.db import models

from .models import Message


def get_messages(user):
    """
    Retrieve messages either sent by or received by the specified user.

    Parameters:
    - user (User): The user for whom to retrieve messages.

    Returns:
    - QuerySet: A queryset containing messages associated with the user, either as sender or receiver.
    """
    return Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user))
