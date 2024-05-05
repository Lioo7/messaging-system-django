from django.db import models
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .utils import get_message
from .models import Message
from .serializers import MessageSerializer
from .filters import MessageFilter


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_class = MessageFilter
    ordering_fields = ['id', 'created_at', 'is_read']

    def get_queryset(self):
        user = self.request.user  # The currently authenticated user
        is_read = self.request.query_params.get('is_read', None)

        queryset = Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user))

        if is_read is not None:
            is_read_bool = is_read.lower() == 'true/'
            queryset = queryset.filter(receiver=user, is_read=is_read_bool)

        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user  # The currently authenticated user
        return Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.receiver == request.user:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender != request.user:
            return Response({"message": "You are not authorized to update this message."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
