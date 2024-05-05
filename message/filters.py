import django_filters

from .models import Message


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['is_read']
