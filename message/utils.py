from django.db import models

from .models import Message


def get_messages(user):
    return Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user))
