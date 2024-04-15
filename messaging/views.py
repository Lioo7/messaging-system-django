from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils import get_message
from .models import Messaging
from .serializers import MessagingSerializer


# Handles writing a new message
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def write_message(request):
    serializer = MessagingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieves all messages for the authenticated user
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    messages = Messaging.objects.filter(receiver=request.user)
    serializer = MessagingSerializer(messages, many=True)
    return Response(serializer.data)


# Retrieves all unread messages for the authenticated user
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_unread_messages(request):
    unread_messages = Messaging.objects.filter(receiver=request.user, is_read=False)
    serializer = MessagingSerializer(unread_messages, many=True)
    return Response(serializer.data)


# Reads a message by its ID, marks it as read, and returns the message data
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def read_message(request, message_id):
    message = get_message(message_id, request.user)
    if message is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message.is_read = True
    message.save()
    serializer = MessagingSerializer(message)
    return Response(serializer.data)


# Deletes a message by its ID
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    message = get_message(message_id, request.user)
    if message is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if message.sender == request.user or message.receiver == request.user:
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
