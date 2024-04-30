from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.reverse import reverse
from .utils import get_message
from .models import Messaging
from .serializers import MessagingSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def index(request):
    """
    Returns a list of all available API endpoints.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Response: HTTP response containing a list of available endpoints.
    """
    endpoints = {
        'write_message': reverse('write_message', request=request),
        'get_all_messages': reverse('get_all_messages', request=request),
        'get_unread_messages': reverse('get_unread_messages', request=request),
        'read_message': reverse('read_message', args=[1], request=request),  # Example with message_id=1
        'delete_message': reverse('delete_message', args=[1], request=request),  # Example with message_id=1
        'token_obtain': reverse('token_obtain_pair', request=request),
        'token_refresh': reverse('token_refresh', request=request),
    }

    return Response({
        'message': 'Welcome to the Messaging System!',
        'endpoints': endpoints
    })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def write_message(request):
    """
    Handles writing a new message.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Response: HTTP response indicating the outcome of the write operation.
    """
    serializer = MessagingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    """
    Retrieves all messages sent or received by the authenticated user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Response: HTTP response containing the list of messages.
    """
    messages = get_message(user=request.user)
    serializer = MessagingSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_unread_messages(request):
    """
    Retrieves all unread messages for the authenticated user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Response: HTTP response containing the list of unread messages.
    """
    unread_messages = Messaging.objects.filter(receiver=request.user, is_read=False)
    serializer = MessagingSerializer(unread_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def read_message(request, message_id):
    """
    Reads a message by its ID, marks it as read if the user is
    the receiver of the message, and returns the message data.

    Parameters:
    - request: The HTTP request object.
    - message_id (int): The ID of the message to read.

    Returns:
    - Response: HTTP response containing the message data.
    """
    message = get_message(message_id=message_id, user=request.user)
    if message is None:
        return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    # If the user is the receiver of the message, mark it as read
    if message.receiver == request.user:
        message.is_read = True
        message.save()
    serializer = MessagingSerializer(message)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    """
    Deletes a message by its ID.

    Parameters:
    - request: The HTTP request object.
    - message_id (int): The ID of the message to delete.

    Returns:
    - Response: HTTP response indicating the outcome of the deletion operation.
    """
    message = get_message(message_id=message_id, user=request.user)
    if message is None:
        return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
    if message.sender == request.user or message.receiver == request.user:
        message.delete()
        return Response({"message": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
